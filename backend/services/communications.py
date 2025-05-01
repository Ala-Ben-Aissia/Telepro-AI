"""
Communications Service

This service handles sending communications through various channels (SMS, email, etc.).
"""

import os
import logging
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)


class SMSService:
    """
    Service for sending SMS messages.

    This service:
    - Sends SMS messages using Twilio
    - Provides methods for testing SMS functionality
    - Logs SMS sending attempts and results
    """

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
    def send_sms(to_number, message):
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
            message = client.messages.create(
                body=message, from_=from_number, to=to_number
            )

            # Log success
            logger.info(f"SMS sent to {to_number}, SID: {message.sid}")

            return {
                "status": "success",
                "message_sid": message.sid,
                "to": to_number,
                "from": from_number,
                "body": message.body,
                "date_sent": message.date_sent.isoformat() if message.date_sent else None,
                "status2": message.status,
            }

        except TwilioRestException as e:
            # Log Twilio-specific error
            logger.error(f"Twilio error sending SMS to {to_number}: {str(e)}")

            return {
                "status": "error",
                "error_code": e.code,
                "error_message": str(e),
                "to": to_number,
            }

        except Exception as e:
            # Log general error
            logger.error(f"Error sending SMS to {to_number}: {str(e)}")

            return {"status": "error", "error_message": str(e), "to": to_number}

    @staticmethod
    def send_test_sms(to_number, message):
        """
        Send a test SMS message.

        This method is specifically for testing purposes and includes
        additional logging and validation.

        Args:
            to_number: Recipient phone number
            message: Message content

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

        # Send the SMS
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
