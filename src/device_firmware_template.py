# Low-Cost Air Sensor Node Firmware Template
# Works on ESP32 (MicroPython)

import network, urequests, time
from machine import Pin, I2C

API_ENDPOINT = "https://your-api-endpoint/upload"

def read_pm_sensor():
    # Replace with your sensor driver
    return {"pm25": 12.1, "pm10": 20.3}

def read_gas_sensor():
    return {"voc": 0.18, "no2": 0.002}

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(1)
    return wlan.ifconfig()

while True:
    pm = read_pm_sensor()
    gas = read_gas_sensor()
    data = {**pm, **gas}

    try:
        r = urequests.post(API_ENDPOINT, json=data)
        print("Uploaded:", r.status_code)
    except:
        print("Upload failed")

    time.sleep(60)
  
