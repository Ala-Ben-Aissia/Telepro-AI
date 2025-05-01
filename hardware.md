# SIM800L/SIM800L v2 Hardware Integration Guide

This guide provides detailed instructions for integrating the SIM800L or SIM800L v2 GSM/GPRS module with the Telepro-AI healthcare communication platform. The integration enables direct SMS sending through hardware, satisfying university project requirements for hardware components.

> **Note**: This guide covers both the original SIM800L and the newer SIM800L v2 modules. Where there are differences between the versions, specific instructions are provided for each variant.

## Table of Contents

1. [Hardware Requirements](#1-hardware-requirements)
2. [Hardware Setup](#2-hardware-setup)
3. [Software Configuration](#3-software-configuration)
4. [Testing the Hardware Connection](#4-testing-the-hardware-connection)
5. [API Integration](#5-api-integration)
6. [Sending SMS Messages](#6-sending-sms-messages)
7. [Troubleshooting](#7-troubleshooting)
8. [Advanced Configuration](#8-advanced-configuration)
9. [References](#9-references)

## 1. Hardware Requirements

### 1.1 SIM800L vs SIM800L v2: Key Differences

Before purchasing components, it's important to understand the differences between the original SIM800L and the newer SIM800L v2 modules:

| Feature           | SIM800L (Original)                   | SIM800L v2                                   |
| ----------------- | ------------------------------------ | -------------------------------------------- |
| Power Supply      | 3.7-4.2V (LiPo battery recommended)  | 5V compatible (can use USB power)            |
| Current Draw      | Up to 2A peak                        | Lower peak current (better power management) |
| Voltage Regulator | External regulator needed            | Built-in voltage regulator                   |
| Antenna           | External antenna required            | Built-in antenna + option for external       |
| SIM Card          | Micro SIM                            | Nano SIM (newer version)                     |
| Form Factor       | Smaller board                        | Slightly larger board with mounting holes    |
| Stability         | More sensitive to power fluctuations | More stable with improved power circuit      |
| Indicator LEDs    | Network status only                  | Network status + power indicator             |

**Which Version to Choose:**

- **SIM800L v2** is recommended for beginners and educational projects due to its easier power requirements and better stability
- **Original SIM800L** may be preferred for size-constrained projects or when using LiPo batteries

### 1.2 Required Components

To complete this integration, you will need the following components:

| Component                    | Purpose                               | Specifications                                                                       | Estimated Cost |
| ---------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------ | -------------- |
| SIM800L or SIM800L v2 Module | Core communication module             | Quad-band 850/900/1800/1900MHz                                                       | $5-15          |
| USB-to-TTL Converter         | Interface between computer and module | CP2102, CH340, or FTDI chip                                                          | $2-5           |
| Power Supply                 | Power the module                      | 3.7-4.2V for SIM800L, 5V for SIM800L v2                                              | $3-8           |
| SIM Card                     | Cellular network access               | Active SIM with SMS capability                                                       | Varies         |
| Jumper Wires                 | Connect components                    | Female-to-female and male-to-female                                                  | $1-3           |
| Breadboard (optional)        | Organize connections                  | Mini breadboard                                                                      | $1-2           |
| Capacitor                    | Stabilize power supply                | 1000μF, 16V electrolytic capacitor (essential for original SIM800L, optional for v2) | $0.50          |

**Important Notes:**

- The original SIM800L module requires a very stable power supply. Voltage drops during transmission can cause the module to reset.
- The SIM800L v2 is more forgiving with power requirements and can often be powered directly from a 5V source.
- The SIM card must be activated and have SMS capability.
- Check your module's SIM card size requirement (micro-SIM for original, typically nano-SIM for v2).

## 2. Hardware Setup

### 2.1 Preparing the SIM800L Module

1. **Insert the SIM card**:

   - Power off the module
   - Locate the SIM card slot on the SIM800L module
   - Insert the SIM card in the correct orientation (usually with the notched corner as indicated on the module)
   - Ensure the SIM card is fully inserted and secure

2. **Prepare the power supply**:
   - The SIM800L requires 3.7-4.2V and can draw up to 2A during transmission
   - Connect the capacitor across the power supply to stabilize voltage:
     - Connect the negative (shorter) leg of the capacitor to GND
     - Connect the positive (longer) leg to VCC

### 2.2 Wiring Diagram

Connect the components as follows:

```
                                  +-------------+
                                  |             |
                                  |   SIM800L   |
                                  |             |
                                  +-------------+
                                   | | | |  | |
                                   | | | |  | |
                                   V V V V  V V
Power Supply (3.7-4.2V) -----------+--+--+--+--+
                                   |  |  |  |  |
USB-to-TTL Converter               |  |  |  |  |
  - VCC (Not Used) ----------------+  |  |  |  |
  - RX ----------------------------|--+  |  |  |
  - TX ----------------------------|-----+  |  |
  - GND ---------------------------|--------+  |
                                   |           |
Capacitor 1000μF                   |           |
  - Positive leg ------------------+           |
  - Negative leg ------------------------------+
```

### 2.3 Step-by-Step Connection Instructions

1. **Connect the USB-to-TTL converter to the SIM800L**:

   - TTL RX → SIM800L TX
   - TTL TX → SIM800L RX
   - TTL GND → SIM800L GND

2. **Connect the power supply**:

   - Positive (+) → SIM800L VCC
   - Negative (-) → SIM800L GND
   - Connect the capacitor in parallel with the power supply (positive to VCC, negative to GND)

3. **Double-check all connections** before powering on the system

4. **Connect the USB-to-TTL converter to your computer**

5. **Power on the SIM800L module**:
   - The network indicator LED on the module should start blinking
   - Fast blinking (once every second): Searching for network
   - Slow blinking (once every 3 seconds): Connected to network

## 3. Software Configuration

### 3.1 Identifying the Serial Port

After connecting the USB-to-TTL converter to your computer, you need to identify which serial port it's using:

**On Windows:**

1. Open Device Manager
2. Expand "Ports (COM & LPT)"
3. Look for "USB-to-Serial" or similar device (e.g., "CP2102 USB to UART Bridge Controller")
4. Note the COM port number (e.g., COM3, COM4)

**On macOS:**

1. Open Terminal
2. Run: `ls /dev/tty.*`
3. Look for something like `/dev/tty.usbserial-XXXXXX` or `/dev/tty.wchusbserialXXXXXXX`

**On Linux:**

1. Open Terminal
2. Run: `ls /dev/ttyUSB*` or `ls /dev/ttyACM*`
3. You should see something like `/dev/ttyUSB0` or `/dev/ttyACM0`

### 3.2 Installing Required Software Dependencies

Ensure you have the required Python packages installed:

```bash
pip install pyserial twilio
```

### 3.3 Updating Environment Variables

Update your `.env` file in the backend directory with the SIM800L configuration:

```
# SMS settings
# Provider can be 'twilio' or 'sim800l'
SMS_PROVIDER=sim800l

# Twilio settings (keep these for fallback)
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# SIM800L hardware settings
SIM800L_PORT=/dev/ttyUSB0  # Update this with your actual port
SIM800L_BAUDRATE=9600
```

Replace `/dev/ttyUSB0` with the actual port you identified in step 3.1.

## 4. Testing the Hardware Connection

Before integrating with the API, it's important to test the direct connection to the SIM800L module.

### 4.1 Using a Serial Terminal

You can use a serial terminal program to send AT commands directly to the module:

**On Windows:**

- Use PuTTY, Arduino IDE Serial Monitor, or Tera Term

**On macOS/Linux:**

- Use screen: `screen /dev/ttyUSB0 9600` (replace with your port)
- Or use minicom: `minicom -D /dev/ttyUSB0 -b 9600`

### 4.2 Basic AT Commands to Test

Once connected to the serial terminal, try these commands:

1. Test basic communication:

   ```
   AT
   ```

   Expected response: `OK`

2. Check signal quality:

   ```
   AT+CSQ
   ```

   Expected response: `+CSQ: XX,XX` (first number is signal strength, 0-31 with 31 being best)

3. Check network registration:

   ```
   AT+CREG?
   ```

   Expected response: `+CREG: 0,1` or `+CREG: 0,5` (indicates registered to network)

4. Set SMS text mode:

   ```
   AT+CMGF=1
   ```

   Expected response: `OK`

5. Send a test SMS (replace with your phone number):
   ```
   AT+CMGS="+1234567890"
   ```
   Type your message, then press Ctrl+Z (or send hex 1A)
   Expected response: `+CMGS: XX` (message reference number)

### 4.3 Exiting the Serial Terminal

- In screen: Press Ctrl+A, then K, then Y
- In minicom: Press Ctrl+A, then X, then Enter

## 5. API Integration

The Telepro-AI platform has been updated to support the SIM800L module through the following components:

### 5.1 SIM800L Class

The `SIM800L` class in `backend/services/communications.py` handles the low-level communication with the hardware:

```python
class SIM800L:
    """Interface for the SIM800L GSM/GPRS module."""

    def __init__(self, port=None, baudrate=9600, timeout=1):
        # Initialize serial connection parameters

    def connect(self):
        # Establish connection to the module

    def send_command(self, command):
        # Send AT commands to the module

    def read_response(self, timeout=5):
        # Read and parse responses from the module

    def send_sms(self, phone_number, message):
        # Send SMS messages through the module
```

### 5.2 SMSService Class

The `SMSService` class provides a unified interface for sending SMS messages through either Twilio or the SIM800L module:

```python
class SMSService:
    """Service for sending SMS messages."""

    @staticmethod
    def get_sms_provider():
        # Determine which provider to use based on settings

    @staticmethod
    def send_sms(to_number, message):
        # Send SMS using the configured provider

    @staticmethod
    def send_test_sms(to_number, message, provider=None):
        # Send a test SMS with optional provider override
```

## 6. Sending SMS Messages

### 6.1 Using the API Endpoint

The platform provides a dedicated endpoint for testing SMS functionality:

**Endpoint:** `POST /api/staff/analytics/test-sms/`

**Request Body:**

```json
{
  "phone_number": "+1234567890", // Replace with recipient's number
  "message": "Test message from SIM800L",
  "provider": "sim800l" // Optional, can be "twilio" or "sim800l"
}
```

**Headers:**

- `Content-Type: application/json`
- `Authorization: Bearer your_jwt_token`

**Sample Response:**

```json
{
  "status": "success",
  "to": "+1234567890",
  "message": "[TEST] Test message from SIM800L",
  "response": "AT+CMGS=\"+1234567890\"\r\n> [TEST] Test message from SIM800L\r\n+CMGS: 24\r\n\r\nOK\r\n",
  "method": "SIM800L",
  "is_test": true,
  "original_message": "[TEST] Test message from SIM800L"
}
```

### 6.2 Using Postman

1. Open Postman
2. Create a new POST request to `http://localhost:8001/api/staff/analytics/test-sms/`
3. Set the headers:
   - Key: `Content-Type`, Value: `application/json`
   - Key: `Authorization`, Value: `Bearer your_jwt_token`
4. Set the request body to raw JSON:
   ```json
   {
     "phone_number": "+1234567890",
     "message": "Test message from SIM800L",
     "provider": "sim800l"
   }
   ```
5. Click Send
6. Check the response and verify that the SMS was received on the target phone

### 6.3 Integration with Campaign Sending

The SIM800L integration works seamlessly with the existing campaign functionality. When `SMS_PROVIDER` is set to `sim800l`, all campaign SMS messages will be sent through the hardware module instead of Twilio.

## 7. Troubleshooting

### 7.1 Hardware Issues

| Problem                         | Possible Causes             | Solutions                                                                                                                                          |
| ------------------------------- | --------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Module not responding           | Power issues                | Check power supply voltage (3.7-4.2V for original, 5V for v2)<br>Ensure capacitor is connected for original SIM800L<br>Check for loose connections |
|                                 | Serial connection issues    | Verify TX/RX connections are correct (and crossed)<br>Try different baud rates<br>Check USB-to-TTL driver installation                             |
|                                 | Module in reset state       | Press reset button on module<br>Power cycle the module                                                                                             |
| Network indicator not blinking  | No power                    | Check power connections<br>For SIM800L v2, check if power LED is on                                                                                |
|                                 | SIM card issues             | Verify SIM is inserted correctly<br>Try SIM in a phone to confirm it's active                                                                      |
| Fast continuous blinking        | Network registration failed | Check SIM card activation<br>Move to area with better signal<br>Try a different network provider                                                   |
| "ERROR" response to AT commands | Incorrect command format    | Check command syntax<br>Ensure proper line endings (CR+LF)                                                                                         |
|                                 | Module busy                 | Wait and try again<br>Reset the module                                                                                                             |
| SMS not sending                 | Network issues              | Check signal strength with AT+CSQ<br>Verify network registration with AT+CREG?                                                                     |
|                                 | Number format issues        | Use international format with + prefix<br>Remove spaces and special characters                                                                     |
|                                 | SIM card issues             | Check SIM card balance<br>Verify SMS service is active                                                                                             |

#### SIM800L v2 Specific Issues

| Problem                           | Possible Causes               | Solutions                                                                                            |
| --------------------------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------- |
| Module powers on but no network   | Built-in antenna insufficient | Connect an external antenna to the U.FL connector if available<br>Move to an area with better signal |
| Power LED on but network LED off  | SIM card not detected         | Re-seat the SIM card<br>Clean SIM card contacts<br>Try a different SIM card                          |
| Module resets during transmission | Power supply insufficient     | Use a power supply capable of providing at least 1A<br>Add a larger capacitor (2200μF)               |

### 7.2 Software Issues

| Problem                               | Possible Causes              | Solutions                                                                          |
| ------------------------------------- | ---------------------------- | ---------------------------------------------------------------------------------- |
| Serial port not found                 | Incorrect port configuration | Double-check port name in .env file<br>Verify port exists in device manager        |
|                                       | Permission issues            | Run application with admin/sudo privileges<br>Check port permissions (Linux/macOS) |
|                                       | Driver issues                | Reinstall USB-to-TTL drivers                                                       |
| "Failed to connect to SIM800L module" | Port busy                    | Close other applications using the port<br>Restart computer                        |
|                                       | Incorrect baud rate          | Try different baud rates (9600, 115200)                                            |
| Timeout errors                        | Slow module response         | Increase timeout settings in SIM800L class                                         |
|                                       | Poor signal                  | Move to area with better reception                                                 |
| API returns error                     | Authentication issues        | Check JWT token<br>Verify user permissions                                         |
|                                       | Invalid request format       | Validate JSON format<br>Check required fields                                      |

## 8. Advanced Configuration

### 8.1 Customizing Timeout Settings

For environments with poor signal or slower response times, you may need to adjust the timeout settings:

```python
# In backend/services/communications.py
class SIM800L:
    def __init__(self, port=None, baudrate=9600, timeout=5):  # Increased from 1 to 5
        # ...

    def read_response(self, timeout=10):  # Increased from 5 to 10
        # ...
```

### 8.2 Setting Up Message Center Number

Some networks require explicitly setting the message center number:

```python
# In backend/services/communications.py, in the send_sms method
# Uncomment and modify these lines:
# self.send_command('AT+CSCA="+1234567890"')  # Replace with your carrier's SMS center
# self.read_response()
```

### 8.3 Implementing Automatic Provider Fallback

For critical messages, you can implement automatic fallback to Twilio if the SIM800L fails:

```python
@staticmethod
def send_sms_with_fallback(to_number, message):
    """Send SMS with automatic fallback to alternative provider."""
    try:
        # Try primary provider
        result = SMSService.send_sms(to_number, message)
        if result["status"] == "error":
            # If failed, try alternative provider
            logger.warning(f"Primary SMS provider failed, trying fallback")
            if SMSService.get_sms_provider() == "sim800l":
                result = SMSService.send_sms_via_twilio(to_number, message)
            else:
                result = SMSService.send_sms_via_sim800l(to_number, message)
        return result
    except Exception as e:
        logger.error(f"Both SMS providers failed: {str(e)}")
        return {"status": "error", "error_message": str(e)}
```

### 8.4 SIM800L v2 Power Saving Mode

The SIM800L v2 supports power saving mode, which can be useful for battery-powered applications:

```python
# Enable power saving mode
self.send_command('AT+CSCLK=1')
self.read_response()

# Disable power saving mode
self.send_command('AT+CSCLK=0')
self.read_response()
```

## 9. References

### 9.1 SIM800L Documentation

- [SIM800L Hardware Design Guide](https://simcom.ee/documents/SIM800/SIM800_Hardware%20Design_V1.09.pdf)
- [SIM800 Series AT Command Manual](https://www.elecrow.com/wiki/images/2/20/SIM800_Series_AT_Command_Manual_V1.09.pdf)
- [SIM800L Datasheet](https://components101.com/sites/default/files/component_datasheet/SIM800L%20Datasheet.pdf)
- [SIM800L v2 Module Documentation](https://lastminuteengineers.com/sim800l-gsm-module-arduino-tutorial/) (includes v2 specifics)

### 9.2 AT Commands Reference

| Command          | Description                | Example               |
| ---------------- | -------------------------- | --------------------- |
| AT               | Test command               | AT                    |
| AT+CSQ           | Check signal quality       | AT+CSQ                |
| AT+CREG?         | Check network registration | AT+CREG?              |
| AT+CMGF=1        | Set SMS text mode          | AT+CMGF=1             |
| AT+CMGS="number" | Send SMS                   | AT+CMGS="+1234567890" |
| AT+CMGL="ALL"    | List all SMS               | AT+CMGL="ALL"         |
| AT+CMGD=index    | Delete SMS                 | AT+CMGD=1             |
| AT+CSCA?         | Check message center       | AT+CSCA?              |
| AT+CSCA="number" | Set message center         | AT+CSCA="+1234567890" |
| AT+CPIN?         | Check SIM status           | AT+CPIN?              |
| AT+CSCLK=1       | Enable power saving        | AT+CSCLK=1            |
| AT+CSCLK=0       | Disable power saving       | AT+CSCLK=0            |

### 9.3 Useful Resources

- [PySerial Documentation](https://pyserial.readthedocs.io/en/latest/pyserial.html)
- [Twilio Python SDK Documentation](https://www.twilio.com/docs/libraries/python)
- [Django Settings Documentation](https://docs.djangoproject.com/en/stable/ref/settings/)
- [SIM800L Tutorial by Last Minute Engineers](https://lastminuteengineers.com/sim800l-gsm-module-arduino-tutorial/)
- [SIM800L v2 vs SIM800L Comparison](https://randomnerdtutorials.com/sim800l-gsm-gprs-module-arduino-tutorial/)
