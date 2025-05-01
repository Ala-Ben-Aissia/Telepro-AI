import serial
import time
import threading


class SIM800LSimulator:
    def __init__(self, port, baudrate=9600):
        self.serial = serial.Serial(port, baudrate)
        self.running = True
        self.thread = threading.Thread(target=self.listen)
        self.thread.daemon = True
        self.thread.start()

    def listen(self):
        while self.running:
            if self.serial.in_waiting:
                command = self.serial.readline().decode("utf-8").strip()
                response = self.process_command(command)
                time.sleep(0.1)  # Simulate processing delay
                self.serial.write((response + "\r\n").encode())

    def process_command(self, command):
        # Simulate AT command responses
        if command == "AT":
            return "OK"
        elif command == "AT+CSQ":
            return "+CSQ: 24,0\r\nOK"  # Simulate good signal strength
        elif command == "AT+CREG?":
            return "+CREG: 0,1\r\nOK"  # Registered to home network
        elif command == "AT+CMGF=1":
            return "OK"
        elif command.startswith("AT+CMGS="):
            # Wait for message content and Ctrl+Z
            time.sleep(0.5)
            return "> "  # Prompt for message
            # In a real implementation, you'd need to handle the message content
            # and respond with +CMGS: <message_reference>\r\nOK
        else:
            return "ERROR"

    def close(self):
        self.running = False
        self.serial.close()


# Usage example
if __name__ == "__main__":
    # Use the virtual port created by socat
    simulator = SIM800LSimulator("/dev/ttys002")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        simulator.close()
