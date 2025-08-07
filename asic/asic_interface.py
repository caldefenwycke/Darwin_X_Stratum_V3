# asic/asic_interface.py
import serial
import time
import json

class AsicInterface:
    def __init__(self, config, stats):
        self.port = config['asic_serial']['port']
        self.baud = config['asic_serial']['baudrate']
        self.stats = stats
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=2)
            time.sleep(2)
        except Exception as e:
            print(f"[ASIC ERROR] Could not open serial port: {e}")
            self.ser = None

    def send_header(self, header_hex):
        if not self.ser:
            return
        try:
            msg = json.dumps({"header": header_hex}) + "\n"
            self.ser.write(msg.encode())
        except Exception as e:
            print(f"[ASIC ERROR] Failed to send header: {e}")

    def wait_for_result(self):
        if not self.ser:
            return None
        try:
            line = self.ser.readline().decode().strip()
            if not line:
                return None
            data = json.loads(line)
            if 'block_found' in data:
                self.stats.submissions += 1
                self.stats.blocks_found += 1
            return data
        except Exception as e:
            print(f"[ASIC ERROR] Failed to receive result: {e}")
            return None
