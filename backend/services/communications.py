"""
Communications Service

This service handles sending communications through various channels (SMS, email, etc.).
It supports both cloud-based services (Twilio) and hardware-based solutions (SIM800L module).
"""

import os
import logging
import time
import serial
import threading
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)


class SIM800L:
    """
    Interface for the SIM800L GSM/GPRS module.

    This class provides methods to interact with the SIM800L module
    for sending SMS messages directly from hardware.
    """

    def __init__(self, port=None, baudrate=9600, timeout=1):
        """
        Initialize the SIM800L interface.

        Args:
            port: Serial port (e.g., '/dev/ttyUSB0', 'COM3')
            baudrate: Baud rate for serial communication
            timeout: Serial timeout in seconds
        """
        self.port = port or getattr(settings, "SIM800L_PORT", "/dev/ttyUSB0")
        self.baudrate = baudrate or getattr(settings, "SIM800L_BAUDRATE", 9600)
        self.timeout = timeout
        self.ser = None
        self.lock = threading.Lock()

    def connect(self):
        """
        Connect to the SIM800L module.

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            self.ser = serial.Serial(
                port=self.port, baudrate=self.baudrate, timeout=self.timeout
            )

            # Initialize the module
            self.send_command("AT")
            response = self.read_response()
            if "OK" not in response:
                logger.error(f"Failed to initialize SIM800L module: {response}")
                return False

            # Set SMS text mode
            self.send_command("AT+CMGF=1")
            response = self.read_response()
            if "OK" not in response:
                logger.error(f"Failed to set SMS text mode: {response}")
                return False

            logger.info("Successfully connected to SIM800L module")
            return True

        except Exception as e:
            logger.error(f"Error connecting to SIM800L module: {str(e)}")
            return False

    def disconnect(self):
        """Close the serial connection to the module."""
        if self.ser and self.ser.is_open:
            self.ser.close()
            logger.info("Disconnected from SIM800L module")

    def send_command(self, command):
        """
        Send an AT command to the module.

        Args:
            command: AT command to send
        """
        if not self.ser or not self.ser.is_open:
            raise ValueError("Serial connection not open")

        # Add carriage return and line feed
        full_command = command + "\r\n"
        self.ser.write(full_command.encode())
        time.sleep(0.5)  # Give the module time to process

    def read_response(self, timeout=5):
        """
        Read the response from the module.

        Args:
            timeout: Maximum time to wait for response in seconds

        Returns:
            str: Response from the module
        """
        if not self.ser or not self.ser.is_open:
            raise ValueError("Serial connection not open")

        response = ""
        start_time = time.time()

        while (time.time() - start_time) < timeout:
            if self.ser.in_waiting:
                line = self.ser.readline().decode("utf-8", errors="ignore").strip()
                response += line + "\n"

                # Check if response is complete
                if line == "OK" or line == "ERROR" or "+CMGS:" in line:
                    break

            time.sleep(0.1)

        return response

    def send_sms(self, phone_number, message):
        """
        Send an SMS message using the SIM800L module.

        Args:
            phone_number: Recipient phone number (with country code)
            message: Message content

        Returns:
            dict: Result of the SMS sending operation
        """
        with self.lock:  # Ensure thread safety
            try:
                if not self.ser or not self.ser.is_open:
                    if not self.connect():
                        return {
                            "status": "error",
                            "error_message": "Failed to connect to SIM800L module",
                            "to": phone_number,
                        }

                # Set message center number if needed
                # self.send_command('AT+CSCA="+1234567890"')
                # self.read_response()

                # Send SMS command
                self.send_command(f'AT+CMGS="{phone_number}"')
                time.sleep(0.5)

                # Send message content
                self.send_command(
                    message + chr(26)
                )  # chr(26) is CTRL+Z, indicates end of message

                # Read response (may take longer for SMS)
                response = self.read_response(timeout=10)

                if "+CMGS:" in response:
                    logger.info(f"SMS sent to {phone_number} via SIM800L module")
                    return {
                        "status": "success",
                        "to": phone_number,
                        "message": message,
                        "response": response,
                        "method": "SIM800L",
                    }
                else:
                    logger.error(f"Failed to send SMS via SIM800L: {response}")
                    return {
                        "status": "error",
                        "error_message": f"Module error: {response}",
                        "to": phone_number,
                    }

            except Exception as e:
                logger.error(f"Error sending SMS via SIM800L: {str(e)}")
                return {"status": "error", "error_message": str(e), "to": phone_number}
            finally:
                # Keep connection open for future messages
                pass


class SMSService:
    """
    Service for sending SMS messages.

    This service:
    - Sends SMS messages using Twilio or SIM800L hardware module
    - Provides methods for testing SMS functionality
    - Logs SMS sending attempts and results
    """

    # Singleton instance of SIM800L
    _sim800l_instance = None

    @staticmethod
    def get_sim800l():
        """
        Get or create a singleton instance of the SIM800L module.

        Returns:
            SIM800L instance
        """
        if SMSService._sim800l_instance is None:
            port = getattr(settings, "SIM800L_PORT", None)
            baudrate = getattr(settings, "SIM800L_BAUDRATE", 9600)

            # Create new instance
            SMSService._sim800l_instance = SIM800L(port=port, baudrate=baudrate)

        return SMSService._sim800l_instance

    @staticmethod
    def get_sms_provider():
        """
        Get the configured SMS provider.

        Returns:
            str: 'twilio' or 'sim800l'
        """
        return getattr(settings, "SMS_PROVIDER", "twilio")

    @staticmethod
    def get_twilio_client():
        """
        Get a Twilio client instance using settings or environment variables.

        Returns:
            Twilio Client instance
        """
        # Try to get credentials from settings
        account_sid = getattr(settings, "TWILIO_ACCOUNT_SID", None)
        auth_token = getattr(settings, "TWILIO_AUTH_TOKEN", None)

        # Fall back to environment variables if not in settings
        if not account_sid:
            account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        if not auth_token:
            auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

        # Check if credentials are available
        if not account_sid or not auth_token:
            raise ValueError(
                "Twilio credentials not found. Please set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN."
            )

        return Client(account_sid, auth_token)

    @staticmethod
    def get_twilio_phone_number():
        """
        Get the Twilio phone number from settings or environment variables.

        Returns:
            Twilio phone number
        """
        # Try to get phone number from settings
        phone_number = getattr(settings, "TWILIO_PHONE_NUMBER", None)

        # Fall back to environment variables if not in settings
        if not phone_number:
            phone_number = os.environ.get("TWILIO_PHONE_NUMBER")

        # Check if phone number is available
        if not phone_number:
            raise ValueError(
                "Twilio phone number not found. Please set TWILIO_PHONE_NUMBER."
            )

        return phone_number

    @staticmethod
    def send_sms_via_sim800l(to_number, message):
        """
        Send an SMS message using the SIM800L hardware module.

        Args:
            to_number: Recipient phone number
            message: Message content

        Returns:
            Dictionary with SMS sending result
        """
        try:
            # Get SIM800L instance
            sim800l = SMSService.get_sim800l()

            # Send the message
            result = sim800l.send_sms(to_number, message)

            return result

        except Exception as e:
            # Log error
            logger.error(f"Error sending SMS via SIM800L to {to_number}: {str(e)}")

            return {
                "status": "error",
                "error_message": str(e),
                "to": to_number,
                "method": "SIM800L",
            }

    @staticmethod
    def send_sms_via_twilio(to_number, message):
        """
        Send an SMS message using Twilio.

        Args:
            to_number: Recipient phone number
            message: Message content

        Returns:
            Dictionary with SMS sending result
        """
        try:
            # Get Twilio client and phone number
            client = SMSService.get_twilio_client()
            from_number = SMSService.get_twilio_phone_number()
            logger.info(f"Sending SMS from {from_number} to {to_number}")
            print("From: ", from_number)
            # Send the message
            message_obj = client.messages.create(
                body=message, from_=from_number, to=to_number
            )

            # Log success
            logger.info(f"SMS sent to {to_number} via Twilio, SID: {message_obj.sid}")

            return {
                "status": "success",
                "message_sid": message_obj.sid,
                "to": to_number,
                "from": from_number,
                "body": message_obj.body,
                "date_sent": message_obj.date_sent.isoformat()
                if message_obj.date_sent
                else None,
                "twilio_status": message_obj.status,
                "method": "Twilio",
            }

        except TwilioRestException as e:
            # Log Twilio-specific error
            logger.error(f"Twilio error sending SMS to {to_number}: {str(e)}")

            return {
                "status": "error",
                "error_code": e.code,
                "error_message": str(e),
                "to": to_number,
                "method": "Twilio",
            }

        except Exception as e:
            # Log general error
            logger.error(f"Error sending SMS via Twilio to {to_number}: {str(e)}")

            return {
                "status": "error",
                "error_message": str(e),
                "to": to_number,
                "method": "Twilio",
            }

    @staticmethod
    def send_sms(to_number, message):
        """
        Send an SMS message using the configured provider.

        Args:
            to_number: Recipient phone number
            message: Message content

        Returns:
            Dictionary with SMS sending result
        """
        # Determine which provider to use
        provider = SMSService.get_sms_provider()

        if provider == "sim800l":
            return SMSService.send_sms_via_sim800l(to_number, message)
        else:
            return SMSService.send_sms_via_twilio(to_number, message)

    @staticmethod
    def send_test_sms(to_number, message, provider=None):
        """
        Send a test SMS message.

        This method is specifically for testing purposes and includes
        additional logging and validation.

        Args:
            to_number: Recipient phone number
            message: Message content
            provider: Optional provider override ('twilio' or 'sim800l')

        Returns:
            Dictionary with test SMS sending result
        """
        # Log test SMS attempt
        logger.info(f"Attempting to send test SMS to {to_number}")

        # Validate phone number format
        if not to_number.startswith("+"):
            logger.warning(
                f"Phone number {to_number} does not start with '+'. Adding it."
            )
            to_number = "+" + to_number

        # Add test prefix to message if not already present
        if not message.startswith("[TEST]"):
            message = "[TEST] " + message

        # Use specified provider or default
        if provider:
            if provider == "sim800l":
                result = SMSService.send_sms_via_sim800l(to_number, message)
            else:
                result = SMSService.send_sms_via_twilio(to_number, message)
        else:
            # Use default provider
            result = SMSService.send_sms(to_number, message)

        # Add test-specific information
        result["is_test"] = True
        result["original_message"] = message

        return result


class EmailService:
    """
    Service for sending email messages.

    This service:
    - Sends email messages
    - Provides methods for testing email functionality
    - Logs email sending attempts and results
    """

    @staticmethod
    def send_email(to_email, subject, message, html_message=None):
        """
        Send an email message.

        Args:
            to_email: Recipient email address
            subject: Email subject
            message: Plain text message content
            html_message: Optional HTML message content

        Returns:
            Dictionary with email sending result
        """
        # This is a placeholder for actual email sending logic
        # In a real implementation, you would use Django's send_mail or a service like SendGrid

        logger.info(f"Email would be sent to {to_email} with subject: {subject}")

        return {
            "status": "success",
            "to": to_email,
            "subject": subject,
            "message_length": len(message),
            "has_html": html_message is not None,
        }

    @staticmethod
    def send_test_email(to_email, subject, message, html_message=None):
        """
        Send a test email message.

        This method is specifically for testing purposes and includes
        additional logging and validation.

        Args:
            to_email: Recipient email address
            subject: Email subject
            message: Plain text message content
            html_message: Optional HTML message content

        Returns:
            Dictionary with test email sending result
        """
        # Log test email attempt
        logger.info(f"Attempting to send test email to {to_email}")

        # Add test prefix to subject if not already present
        if not subject.startswith("[TEST]"):
            subject = "[TEST] " + subject

        # Send the email
        result = EmailService.send_email(to_email, subject, message, html_message)

        # Add test-specific information
        result["is_test"] = True
        result["original_subject"] = subject

        return result
