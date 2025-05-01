"""Mock implementation of SIM800L for testing without hardware."""

import threading
import time
import random


class MockSIM800L:
    """Mock implementation of SIM800L for testing without hardware."""

    def __init__(self, port=None, baudrate=9600, timeout=1):
        self.connected = False
        self.lock = threading.Lock()
        self.last_command = None

    def connect(self):
        """Simulate connecting to the module."""
        self.connected = True
        return True

    def disconnect(self):
        """Simulate disconnecting from the module."""
        self.connected = False

    def send_command(self, command):
        """Simulate sending AT commands."""
        # Just log the command in development
        print(f"[MOCK SIM800L] Command sent: {command}")

    def read_response(self, timeout=5):
        """Simulate reading responses."""
        # Simulate processing delay
        time.sleep(0.2)

        # Return appropriate mock responses based on common commands
        if "AT" == self.last_command:
            return "OK\r\n"
        elif "AT+CSQ" in self.last_command:
            return "+CSQ: 25,0\r\nOK\r\n"
        elif "AT+CREG?" in self.last_command:
            return "+CREG: 0,1\r\nOK\r\n"
        elif "AT+CMGF=1" in self.last_command:
            return "OK\r\n"
        elif "AT+CMGS=" in self.last_command:
            # Simulate message sending
            msg_ref = random.randint(1, 100)
            return f"+CMGS: {msg_ref}\r\n\r\nOK\r\n"
        else:
            return "OK\r\n"

    def send_sms(self, phone_number, message):
        """Simulate sending an SMS message."""
        with self.lock:
            print(f"[MOCK SIM800L] Sending SMS to {phone_number}: {message}")

            # Simulate success with 90% probability
            if random.random() < 0.9:
                msg_ref = random.randint(1, 100)
                return {
                    "status": "success",
                    "to": phone_number,
                    "message": message,
                    "response": f'AT+CMGS="{phone_number}"\r\n> {message}\r\n+CMGS: {msg_ref}\r\n\r\nOK\r\n',
                    "method": "SIM800L",
                }
            else:
                # Simulate occasional failure
                return {
                    "status": "error",
                    "error_message": "Network timeout",
                    "to": phone_number,
                    "method": "SIM800L",
                }
