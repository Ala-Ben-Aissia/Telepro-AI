# tests/test_sms_service.py
from django.test import TestCase
from services.communications import SMSService


class SMSServiceTests(TestCase):
    def test_send_sms(self):
        result = SMSService.send_sms("+1234567890", "Test message")
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["method"], "SIM800L")
