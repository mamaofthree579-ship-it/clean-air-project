# Firmware Setup Guide
This guide explains how to install, configure, and deploy firmware for the Clean Air Project Community Air Sensor Node.

---

# 1️⃣ Requirements

## Hardware
- ESP32 (recommended) or ESP8266  
- USB data cable  
- Sensors wired per the wiring guide  

## Software
Install these:

### Option A — Arduino IDE
https://www.arduino.cc/en/software

### Option B — PlatformIO (VS Code)
https://platformio.org/install

---

# 2️⃣ Install Board Definitions

## ESP32 (Arduino IDE)
1. Go to **File → Preferences**  
2. Add this URL under “Additional Board URLs”:  
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
3. Go to **Tools → Board Manager**  
4. Search for **ESP32** and install.

---

# 3️⃣ Install Required Libraries

Install these via Library Manager:

- Adafruit BME280  
- Adafruit SHT31 (if used)  
- PubSubClient (MQTT)  
- ArduinoJson  
- PMS Library  
- WiFi (built-in)

---

# 4️⃣ Configure Firmware

Open the file:

```
src/firmware/config.h
```

Set Wi-Fi:

```cpp
#define WIFI_SSID "YourNetwork"
#define WIFI_PASSWORD "YourPassword"
```

Set data destination:

```cpp
#define MQTT_SERVER "your_server_ip"
#define MQTT_TOPIC "community/air/your_node_id"
```

Or set the HTTP POST endpoint:

```cpp
#define API_ENDPOINT "https://your-server.com/api/airdata"
```

---

# 5️⃣ Flash Firmware

### Using Arduino IDE:
- Choose **Board: ESP32 Dev Module**
- Select **Port**
- Click **Upload**

### Using PlatformIO:
```
pio run --target upload
```

---

# 6️⃣ Verify Operation

Open Serial Monitor:

```
115200 baud
```

Look for:

```
WiFi connected!
PMS OK
BME OK
Publishing PM2.5: XX
```

If data appears, your node is online.

---

# ✔ Firmware installation complete!
Your sensor node is now transmitting live data.
