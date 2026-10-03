import serial
import time

esp32 = serial.Serial("COM7", 115200, timeout=1)

time.sleep(2)

print("Connected to ESP32")
print("Waiting for direction...")

while True:
    data = esp32.readline().decode().strip()

    if data:
        print("Received:", data)