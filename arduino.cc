#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <SoftwareSerial.h>

// WiFi credentials
const char* ssid = "my_wifi_ssid";
const char* password = "my_wifi_password";

// Django server settings
const char* serverUrl = "http://192.168.1.100:8000/api/staff/analytics/test-sms/";
const char* authToken = "your_jwt_token"; // Add your JWT token here

// SIM800L v2 settings
#define SIM800L_RX 10  // Connect to TX of SIM800L
#define SIM800L_TX 11  // Connect to RX of SIM800L
SoftwareSerial sim800l(SIM800L_RX, SIM800L_TX);

// Passive buzzer pin
#define BUZZER_PIN 5

// Tone frequencies for different notifications
#define TONE_SUCCESS 1000  // 1000 Hz
#define TONE_ERROR 500     // 500 Hz
#define TONE_WAITING 700   // 700 Hz
#define TONE_CONNECTED 1500 // 1500 Hz

void setup() {
  Serial.begin(115200);
  sim800l.begin(9600);
  
  // Initialize buzzer
  pinMode(BUZZER_PIN, OUTPUT);
  
  // Play startup tone
  playStartupTone();
  
  // Connect to Wi-Fi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  
  // Play waiting tone while connecting to WiFi
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    tone(BUZZER_PIN, TONE_WAITING, 100);
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected to WiFi");
    playConnectedTone();
  } else {
    Serial.println("\nFailed to connect to WiFi");
    playErrorTone();
  }
  
  // Initialize SIM800L
  Serial.println("Initializing SIM800L...");
  delay(1000);
  sim800l.println("AT");
  delay(500);
  if (sim800l.available()) {
    String response = sim800l.readString();
    Serial.println(response);
    if (response.indexOf("OK") >= 0) {
      Serial.println("SIM800L initialized successfully");
      playSuccessTone();
      
      // Set SMS text mode
      sim800l.println("AT+CMGF=1");
      delay(500);
      sim800l.readString(); // Clear buffer
    } else {
      Serial.println("Failed to initialize SIM800L");
      playErrorTone();
    }
  } else {
    Serial.println("No response from SIM800L");
    playErrorTone();
  }
  
  // Example: Send an SMS with a specific provider
  String phoneNumber = "+121622583473";
  String message = "Test message from ESP32";
  String provider = "sim800l"; // Options: "twilio" or "sim800l"
  
  if (sendSms(phoneNumber, message, provider)) {
    Serial.println("SMS sent successfully");
    playSuccessMelody();
  } else {
    Serial.println("Failed to send SMS");
    playErrorMelody();
  }
}

void loop() {
  // Add more logic here if needed
  delay(10000);
}

bool sendSms(String phoneNumber, String message, String provider) {
  if (provider == "twilio" || provider == "api") {
    return sendSmsViaApi(phoneNumber, message, provider);
  } else if (provider == "sim800l") {
    return sendSmsViaSim800l(phoneNumber, message);
  } else {
    Serial.println("Unknown provider: " + provider);
    return false;
  }
}

bool sendSmsViaApi(String phoneNumber, String message, String provider) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected");
    return false;
  }
  
  // Play waiting tone
  tone(BUZZER_PIN, TONE_WAITING, 200);
  
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", "Bearer " + String(authToken));
  
  // Create JSON payload
  StaticJsonDocument<256> doc;
  doc["phone_number"] = phoneNumber;
  doc["message"] = message;
  doc["provider"] = provider;
  String requestBody;
  serializeJson(doc, requestBody);
  
  // Send POST request
  int httpResponseCode = http.POST(requestBody);
  
  if (httpResponseCode == 200) {
    String response = http.getString();
    DynamicJsonDocument resDoc(1024);
    DeserializationError error = deserializeJson(resDoc, response);
    
    if (!error && resDoc["status"] == "success") {
      Serial.println("SMS sent successfully via API with " + provider);
      http.end();
      return true;
    } else {
      Serial.println("Failed to send SMS via API: " + response);
      http.end();
      return false;
    }
  } else {
    Serial.println("HTTP error: " + String(httpResponseCode));
    http.end();
    return false;
  }
}

bool sendSmsViaSim800l(String phoneNumber, String message) {
  // Play waiting tone
  tone(BUZZER_PIN, TONE_WAITING, 200);
  
  // Set SMS text mode
  sim800l.println("AT+CMGF=1");
  delay(500);
  sim800l.readString(); // Clear buffer
  
  // Send SMS command
  sim800l.print("AT+CMGS=\"");
  sim800l.print(phoneNumber);
  sim800l.println("\"");
  delay(500);
  
  // Check for ">" prompt
  String response = sim800l.readString();
  if (response.indexOf(">") < 0) {
    Serial.println("Failed to get prompt for SMS");
    return false;
  }
  
  // Send message content and Ctrl+Z (ASCII 26) to end
  sim800l.print(message);
  sim800l.write(26);
  
  // Play processing tone
  for (int i = 0; i < 3; i++) {
    tone(BUZZER_PIN, TONE_WAITING + (i * 50), 200);
    delay(300);
  }
  
  delay(3000); // Wait for the module to process
  
  // Check response
  response = sim800l.readString();
  Serial.println("SIM800L response: " + response);
  
  if (response.indexOf("OK") >= 0 || response.indexOf("+CMGS") >= 0) {
    Serial.println("SMS sent successfully via SIM800L");
    return true;
  } else {
    Serial.println("Failed to send SMS via SIM800L");
    return false;
  }
}

// Sound patterns for different events
void playStartupTone() {
  // Play ascending tones
  for (int i = 0; i < 3; i++) {
    tone(BUZZER_PIN, 500 + (i * 200), 150);
    delay(200);
  }
  noTone(BUZZER_PIN);
}

void playConnectedTone() {
  // Play two high tones
  tone(BUZZER_PIN, TONE_CONNECTED, 100);
  delay(150);
  tone(BUZZER_PIN, TONE_CONNECTED, 100);
  delay(100);
  noTone(BUZZER_PIN);
}

void playSuccessTone() {
  // Play a single success tone
  tone(BUZZER_PIN, TONE_SUCCESS, 200);
  delay(200);
  noTone(BUZZER_PIN);
}

void playErrorTone() {
  // Play a single error tone
  tone(BUZZER_PIN, TONE_ERROR, 300);
  delay(300);
  noTone(BUZZER_PIN);
}

void playSuccessMelody() {
  // Play ascending success melody
  int successNotes[] = {TONE_SUCCESS, TONE_SUCCESS + 200, TONE_SUCCESS + 400};
  int noteDurations[] = {150, 150, 250};
  
  for (int i = 0; i < 3; i++) {
    tone(BUZZER_PIN, successNotes[i], noteDurations[i]);
    delay(noteDurations[i] + 50);
  }
  noTone(BUZZER_PIN);
}

void playErrorMelody() {
  // Play descending error melody
  int errorNotes[] = {TONE_ERROR + 300, TONE_ERROR + 150, TONE_ERROR};
  int noteDurations[] = {150, 150, 300};
  
  for (int i = 0; i < 3; i++) {
    tone(BUZZER_PIN, errorNotes[i], noteDurations[i]);
    delay(noteDurations[i] + 50);
  }
  noTone(BUZZER_PIN);
}
