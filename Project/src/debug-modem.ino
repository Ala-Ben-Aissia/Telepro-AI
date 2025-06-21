#define SIM800L_IP5306_VERSION_20200811

// Define the serial console for debug prints
#define DUMP_AT_COMMANDS
#define TINY_GSM_DEBUG SerialMon

#include "utilities.h"
#include "pitches.h"

// Set serial for debug console (Serial Monitor, 115200 baud)
#define SerialMon Serial
// Set serial for AT commands (to SIM800L)
#define SerialAT Serial1
#define BUZZER_PIN 2

// Configure TinyGSM library
#define TINY_GSM_MODEM_SIM800   // Modem is SIM800
#define TINY_GSM_RX_BUFFER 1024 // Set RX buffer to 1Kb

#include <TinyGsmClient.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Timeouts and retry configurations
#define WIFI_CONNECT_TIMEOUT 20000 // 20 seconds for WiFi connection
#define MODEM_INIT_TIMEOUT 10000   // 10 seconds for modem initialization
#define API_REQUEST_TIMEOUT 10000  // 10 seconds for API requests
#define MAX_RETRIES 3              // Maximum number of retries for operations
#define CALL_CONNECT_TIMEOUT 30000 // 30 seconds for call connection
#define CALL_DURATION 60000        // 60 seconds max call duration

#ifdef DUMP_AT_COMMANDS
#include <StreamDebugger.h>
#include "endpoints.h"
StreamDebugger debugger(SerialAT, SerialMon);
TinyGsm modem(debugger);
#else
TinyGsm modem(SerialAT);
#endif

// Configuration
const char *ssid = "ORANGE_9BF6";
const char *password = "DXKTF882";
#define SMS_TARGET "+21622492052"
#define CALL_TARGET "+21622492052"
// #define SMS_TARGET "+21628986530"
// #define CALL_TARGET "+21628986530"

bool hasBeenContacted = false;

// Patient data structure
struct Patient
{
  String username;
  String password;
  String phone_number;
  String uuid;
  String preferred_contact_methods;
};

// Patient instances
Patient patient9 = {
    "patient9",
    "PatientPass123!",
    SMS_TARGET,
    "367a4697-2704-4ec6-8b6b-9b966fd40ce8",
    "SMS",
};

Patient patient13 = {
    "patient13",
    "PatientPass123!",
    CALL_TARGET,
    "e48b4af2-9f54-454b-9f72-a9114baa2ba6",
    "CALL",
};

// Function prototypes
bool connectToWiFi();
bool initializeModem();
bool checkNetworkRegistration();
int getSignalQualityWithRetry();
bool checkOperator();
void configureAudio();
bool makeCall(const char *target);
String login(const String &username, const String &password);
String contactPatient(const String &authToken, const String &recipientNumber, const String &contactMethod);
void playCallTone();
void playErrorTone();
void playLoginTone();
void playSMSTone();

void setup()
{
  // Initialize Serial Monitor
  SerialMon.begin(115200);
  delay(100);
  SerialMon.println("\n--- SIM800L Call/SMS System Starting ---");

  // Start power management
  if (setupPMU() == false)
  {
    SerialMon.println("ERROR: Power management setup failed");
    playErrorTone();
    while (true)
    {
      delay(1000);
    }
  }

  // Setup modem hardware
  setupModem();

  // Set modem baud rate and UART pins
  SerialAT.begin(115200, SERIAL_8N1, MODEM_RX, MODEM_TX);
  delay(1000);

  // Initialize modem
  if (!initializeModem())
  {
    SerialMon.println("ERROR: Modem initialization failed");
    playErrorTone();
    while (true)
    {
      delay(1000);
    }
  }

  // Connect to WiFi
  if (!connectToWiFi())
  {
    SerialMon.println("ERROR: WiFi connection failed");
    playErrorTone();
    // Continue with cellular operations even if WiFi fails
  }

  // Check essential network operations
  if (!checkNetworkRegistration())
  {
    SerialMon.println("ERROR: Network registration failed");
    playErrorTone();
    while (true)
    {
      delay(1000);
    }
  }

  int signalQuality = getSignalQualityWithRetry();
  if (signalQuality < 10 || signalQuality > 31)
  {
    SerialMon.println("ERROR: Signal quality inadequate");
    playErrorTone();
    while (true)
    {
      delay(1000);
    }
  }

  if (!checkOperator())
  {
    SerialMon.println("ERROR: Operator check failed");
    playErrorTone();
    while (true)
    {
      delay(1000);
    }
  }

  // Configure audio settings
  configureAudio();

  SerialMon.println("Setup complete - system ready");
}

void loop()
{
  // Run only once
  static bool hasRun = false;
  if (hasRun)
  {
    delay(1000);
    return;
  }
  hasRun = true;

  // Log current time
  unsigned long timestamp = millis();
  SerialMon.println("\n[Time: " + String(timestamp) + " ms] Starting main operation...");

  // Use patient9 for this run
  // Patient currentPatient = patient9; // sms
  Patient currentPatient = patient13; // call

  // Attempt login
  String authToken = login(currentPatient.username, currentPatient.password);
  if (authToken.startsWith("Error"))
  {
    SerialMon.println(authToken);
    playErrorTone();
  }
  else
  {
    playLoginTone(); // logged in successfully

    if (!hasBeenContacted)
    {
      hasBeenContacted = true;

      // Contact patient according to their preferred method
      if (currentPatient.preferred_contact_methods == "SMS")
      {
        SerialMon.println("Contacting patient via SMS as per preference");
        String contactResult = contactPatient(authToken, currentPatient.phone_number, "SMS");
        SerialMon.println("SMS result: " + contactResult);

        if (contactResult.indexOf("successfully") >= 0)
        {
          playSMSTone();
        }
        else
        {
          playErrorTone();
        }
      }
      else if (currentPatient.preferred_contact_methods == "CALL")
      {
        SerialMon.println("Contacting patient via call as per preference");
        // First log the call to the server
        String contactResult = contactPatient(authToken, currentPatient.phone_number, "CALL");
        SerialMon.println("Call logging result: " + contactResult);

        // Then make the actual call
        SerialMon.println("Attempting call to: " + currentPatient.phone_number);
        if (!makeCall(currentPatient.phone_number.c_str()))
        {
          SerialMon.println("Call attempt failed");
          playErrorTone();
        }
      }
    }
  }

  // Operation completed
  SerialMon.println("Operation completed, entering idle state...");

  // Instead of halting, keep the device running for potential future operations
  while (true)
  {
    // Check for incoming calls or messages
    String response;
    SerialAT.println("AT+CPAS");
    if (modem.waitResponse(1000, response))
    {
      if (response.indexOf("+CPAS: 3") >= 0)
      { // Incoming call
        SerialMon.println("Incoming call detected");
        // Handle incoming call here if needed
      }
    }

    // Check for SMS
    if (modem.waitResponse(100, "+CMTI:"))
    {
      SerialMon.println("Incoming SMS detected");
      // Handle incoming SMS here if needed
    }

    delay(5000); // Check every 5 seconds
  }
}

bool initializeModem()
{
  // Restart modem to clear state
  SerialMon.println("Restarting modem...");
  modem.restart();
  delay(3000);

  // Flush Serial buffers
  while (SerialAT.available())
  {
    SerialAT.read();
  }

  // Initialize modem with timeout
  SerialMon.println("Initializing modem...");
  unsigned long startTime = millis();

  while (millis() - startTime < MODEM_INIT_TIMEOUT)
  {
    if (modem.init())
    {
      SerialMon.println("Modem initialized successfully");

      // Set auto operator selection
      SerialMon.println("Setting auto operator selection...");
      SerialAT.println("AT+COPS=0");
      delay(1000);
      String copsResponse;
      if (modem.waitResponse(1000, copsResponse))
      {
        SerialMon.println("COPS Init: " + copsResponse);
      }

      // Ensure full functionality
      SerialAT.println("AT+CFUN=1");
      delay(1000);
      String cfunResponse;
      if (modem.waitResponse(1000, cfunResponse))
      {
        SerialMon.println("CFUN Init: " + cfunResponse);
      }

      // Get modem info
      SerialMon.println("Modem Info:");
      SerialMon.println("  Manufacturer: " + modem.getModemInfo());
      SerialMon.println("  Model: " + modem.getModemName());

      return true;
    }

    delay(1000);
    SerialMon.println("Retrying modem initialization...");
  }

  return false;
}

bool connectToWiFi()
{
  SerialMon.print("Connecting to Wi-Fi network: ");
  SerialMon.println(ssid);

  WiFi.begin(ssid, password);

  unsigned long startAttemptTime = millis();

  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < WIFI_CONNECT_TIMEOUT)
  {
    delay(500);
    SerialMon.print(".");
  }

  if (WiFi.status() == WL_CONNECTED)
  {
    SerialMon.println("\nWi-Fi connected successfully.");
    SerialMon.print("Assigned IP Address: ");
    SerialMon.println(WiFi.localIP());
    return true;
  }
  else
  {
    SerialMon.println("\nFailed to connect to Wi-Fi network.");
    // Try connecting again
    WiFi.disconnect();
    delay(1000);
    WiFi.begin(ssid, password);

    startAttemptTime = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < WIFI_CONNECT_TIMEOUT)
    {
      delay(500);
      SerialMon.print(".");
    }

    if (WiFi.status() == WL_CONNECTED)
    {
      SerialMon.println("\nWi-Fi connected on second attempt.");
      SerialMon.print("Assigned IP Address: ");
      SerialMon.println(WiFi.localIP());
      return true;
    }

    return false;
  }
}

bool checkNetworkRegistration()
{
  SerialMon.print("Checking network registration: ");

  for (int retry = 0; retry < MAX_RETRIES; retry++)
  {
    String cregResponse;
    SerialAT.println("AT+CREG?");

    if (modem.waitResponse(5000, cregResponse))
    {
      if (cregResponse.indexOf("+CREG: 0,1") >= 0 || cregResponse.indexOf("+CREG: 0,5") >= 0)
      {
        SerialMon.println("Registered (" + cregResponse + ")");
        return true;
      }
      else if (cregResponse.indexOf("+CREG: 0,2") >= 0)
      {
        SerialMon.println("Searching (" + cregResponse + ")");
      }
      else
      {
        SerialMon.println("Not registered (" + cregResponse + ")");
      }
    }
    else
    {
      SerialMon.println("ERROR: No response from AT+CREG?");
    }

    delay(2000); // Wait before retry
    SerialMon.print("Retry " + String(retry + 1) + "... ");
  }

  return false;
}

int getSignalQualityWithRetry()
{
  SerialMon.print("Checking signal quality: ");

  int signalQuality = -1;
  for (int retry = 0; retry < MAX_RETRIES; retry++)
  {
    signalQuality = modem.getSignalQuality();

    if (signalQuality != 99 && signalQuality >= 0)
    {
      int rssi = -113 + 2 * signalQuality; // Convert to dBm
      SerialMon.println(String(signalQuality) + " (RSSI: " + String(rssi) + " dBm)");
      return signalQuality;
    }

    SerialMon.println("Invalid signal quality: " + String(signalQuality) + ", retrying...");
    delay(1000);
  }

  SerialMon.println("Failed to get valid signal quality after " + String(MAX_RETRIES) + " attempts");
  return signalQuality;
}

bool checkOperator()
{
  SerialMon.print("Checking operator: ");

  for (int retry = 0; retry < MAX_RETRIES; retry++)
  {
    String copsResponse;
    SerialAT.println("AT+COPS?");

    if (modem.waitResponse(5000, copsResponse))
    {
      if (copsResponse.indexOf("+COPS:") >= 0)
      {
        SerialMon.println(copsResponse);
        return true;
      }
      else
      {
        SerialMon.println("No operator (" + copsResponse + ")");
      }
    }
    else
    {
      SerialMon.println("ERROR: No response from AT+COPS?");
    }

    delay(2000); // Wait before retry
    SerialMon.print("Retry " + String(retry + 1) + "... ");
  }

  return false;
}

void configureAudio()
{
  SerialMon.println("Configuring modem audio...");

  // Send commands and check responses
  SerialAT.println("AT+CHFA=1"); // Swap audio channels
  modem.waitResponse(200);

  SerialAT.println("AT+CRSL=100"); // Ringer volume
  modem.waitResponse(200);

  SerialAT.println("AT+CLVL=100"); // Speaker volume
  modem.waitResponse(200);

  SerialAT.println("AT+CLIP=1"); // Caller ID
  modem.waitResponse(200);

  SerialMon.println("Audio configuration complete");
}

bool makeCall(const char *target)
{
  SerialMon.println("Initiating call to: " + String(target));

  bool callInitiated = modem.callNumber(target);
  if (!callInitiated)
  {
    SerialMon.println("Failed to initiate call");
    String atResponse;
    SerialAT.println("AT+CEER");
    if (modem.waitResponse(1000, atResponse))
    {
      SerialMon.println("Call Error: " + atResponse);
    }
    return false;
  }

  SerialMon.println("Call initiated, waiting for connection...");

  // Wait for call to connect or timeout
  unsigned long startTime = millis();
  bool callActive = false;

  while (millis() - startTime < CALL_CONNECT_TIMEOUT)
  {
    String response;
    SerialAT.println("AT+CPAS");

    if (modem.waitResponse(1000, response))
    {
      SerialMon.println("CPAS: " + response);
      if (response.indexOf("+CPAS: 4") >= 0)
      { // Call in progress
        SerialMon.println("Call connected successfully");
        callActive = true;
        playCallTone();
        break;
      }
    }

    delay(1000);
  }

  if (!callActive)
  {
    SerialMon.println("Call failed to connect within timeout");
    String atResponse;
    SerialAT.println("AT+CEER");
    if (modem.waitResponse(1000, atResponse))
    {
      SerialMon.println("Call Error: " + atResponse);
    }
    modem.callHangup();
    return false;
  }

  // Monitor call for duration or until hangup
  startTime = millis();
  while (millis() - startTime < CALL_DURATION)
  {
    String response;
    SerialAT.println("AT+CPAS");

    if (modem.waitResponse(1000, response))
    {
      SerialMon.println("CPAS: " + response);
      if (response.indexOf("+CPAS: 0") >= 0)
      { // Phone idle
        SerialMon.println("Call ended");
        break;
      }
    }

    delay(2000); // Check less frequently to reduce AT command load
  }

  // Ensure call is hung up
  modem.callHangup();
  SerialMon.println("Call completed");

  return true;
}

String login(const String &username, const String &password)
{
  HTTPClient http;

  // Ensure WiFi is connected
  if (WiFi.status() != WL_CONNECTED)
  {
    return "Error: WiFi not connected";
  }

  const int res = http.begin(loginUrl);
  if (res == 0)
  {
    return "Error: Failed to connect to server";
  }

  http.addHeader("Content-Type", "application/json");
  http.setTimeout(API_REQUEST_TIMEOUT);

  String payload = "{\"username\":\"" + username + "\",\"password\":\"" + password + "\"}";
  int statusCode = http.POST(payload);

  if (statusCode == HTTP_CODE_OK || statusCode == HTTP_CODE_BAD_REQUEST)
  {
    String response = http.getString();
    http.end();

    JsonDocument doc;
    DeserializationError error = deserializeJson(doc, response);

    if (!error)
    {
      if (statusCode == HTTP_CODE_BAD_REQUEST)
      {
        if (doc["detail"])
        {
          String errorDetail = doc["detail"];
          return "Error: " + errorDetail;
        }
        return "Error: Invalid credentials";
      }

      if (doc["access"])
      {
        String accessToken = doc["access"];
        return accessToken;
      }
      else
      {
        return "Error: Access token not found in response";
      }
    }

    return "Error: JSON parsing failed: " + String(error.c_str());
  }

  http.end();
  return "Error: Login failed with status code " + String(statusCode);
}

String contactPatient(const String &authToken, const String &recipientNumber, const String &contactMethod)
{
  if (contactMethod != "SMS" && contactMethod != "CALL")
  {
    return "Error: Invalid contact method specified";
  }

  // First, log the contact attempt to the server (if WiFi is available)
  if (WiFi.status() == WL_CONNECTED)
  {
    HTTPClient http;

    if (!http.begin(smsUrl))
    {
      SerialMon.println("Warning: Failed to connect to API endpoint");
      // Continue with SMS/call even if server logging fails
    }
    else
    {
      String message = "This is a test message.";
      String payload = "{\"phone_number\": \"" + recipientNumber +
                       "\", \"message\": \"" + message + "\"}";

      SerialMon.println("API Request payload: " + payload);

      http.addHeader("Content-Type", "application/json");
      http.addHeader("Authorization", "Bearer " + authToken);
      http.setTimeout(API_REQUEST_TIMEOUT);

      int statusCode = http.POST(payload);
      String response = http.getString();

      SerialMon.println("API Status: " + String(statusCode));
      SerialMon.println("API Response: " + response);

      http.end();
    }
  }

  // Now perform the actual contact via SIM800L only for SMS
  // Call operation is handled separately in makeCall function
  if (contactMethod == "SMS")
  {
    String message = "This is a test SMS message. Please reply to confirm receipt.";
    bool contactSuccess = modem.sendSMS(recipientNumber.c_str(), message.c_str());
    return contactSuccess ? "SMS sent successfully!" : "Error: Failed to send SMS!";
  }
  else
  {
    // For CALL, we just log it and return success - actual call is handled separately
    return "Call logging successful";
  }
}

// Music and tone functions
int melody[] = {
    NOTE_E5, NOTE_D5, NOTE_FS4, NOTE_GS4,
    NOTE_CS5, NOTE_B4, NOTE_D4, NOTE_E4,
    NOTE_B4, NOTE_A4, NOTE_CS4, NOTE_E4,
    NOTE_A4};

int durations[] = {
    8, 8, 4, 4,
    8, 8, 4, 4,
    8, 8, 4, 4,
    2};

int loginMelody[] = {262, 330, 392, 523};
int loginDurations[] = {4, 4, 4, 2};

int messageMelody[] = {392, 440, 494};
int messageDurations[] = {8, 8, 4};

void playCallTone()
{
  delay(5000); // delay to get the real call
  int size = sizeof(durations) / sizeof(int);
  // Play just one cycle of the melody to avoid blocking for too long
  for (int i = 0; i < 5; i++)
  {
    for (int note = 0; note < size; note++)
    {
      int duration = 1000 / durations[note];
      tone(BUZZER_PIN, melody[note], duration);

      int pauseBetweenNotes = duration * 1.30;
      delay(pauseBetweenNotes);
      noTone(BUZZER_PIN);
    }
    delay(1000);
  }
}

void playErrorTone()
{
  int errorNotes[] = {NOTE_A5, NOTE_E5, NOTE_A4};
  int errorDurations[] = {8, 8, 4};

  for (int i = 0; i < 3; i++)
  {
    int duration = 1000 / errorDurations[i];
    tone(BUZZER_PIN, errorNotes[i], duration);

    int pauseBetween = duration * 1.30;
    delay(pauseBetween);
    noTone(BUZZER_PIN);
  }
}

void playLoginTone()
{
  int size = sizeof(loginDurations) / sizeof(int);

  for (int note = 0; note < size; note++)
  {
    int duration = 1000 / loginDurations[note];
    tone(BUZZER_PIN, loginMelody[note], duration);

    int pauseBetweenNotes = duration * 1.30;
    delay(pauseBetweenNotes);
    noTone(BUZZER_PIN);
  }

  delay(500); // Shorter pause after melody
}

void playSMSTone()
{
  int size = sizeof(messageDurations) / sizeof(int);

  for (int note = 0; note < size; note++)
  {
    int duration = 1000 / messageDurations[note];
    tone(BUZZER_PIN, messageMelody[note], duration);

    int pauseBetweenNotes = duration * 1.30;
    delay(pauseBetweenNotes);
    noTone(BUZZER_PIN);
  }

  delay(500); // Shorter pause after melody
}