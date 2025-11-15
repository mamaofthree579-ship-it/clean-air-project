"""
Device Provisioning Script
Registers a device, writes credentials over serial, and verifies connectivity.
"""

import json
import time
import serial
import requests

API_URL = "https://your-server/register-device"

def register_device(device_id: str):
    payload = {"device_id": device_id}
    print(f"Registering device {device_id}…")
    r = requests.post(API_URL, json=payload)
    r.raise_for_status()
    return r.json()

def write_credentials(port, ssid, password, token):
    print("Writing credentials over serial…")
    ser = serial.Serial(port, 115200, timeout=3)
    time.sleep(2)
    ser.write(f"SSID:{ssid}\n".encode())
    ser.write(f"PASS:{password}\n".encode())
    ser.write(f"TOKEN:{token}\n".encode())
    ser.close()
    print("Done.")

if __name__ == "__main__":
    device_id = input("Device ID: ")
    port = input("Serial port (e.g., /dev/ttyUSB0): ")
    ssid = input("WiFi SSID: ")
    password = input("WiFi password: ")

    resp = register_device(device_id)
    write_credentials(port, ssid, password, resp["token"])

    print("Provisioning completed successfully.")
