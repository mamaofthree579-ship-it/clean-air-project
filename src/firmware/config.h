#ifndef CONFIG_H
#define CONFIG_H

// --- WIFI ---
#define WIFI_SSID "YOUR_WIFI_NAME"
#define WIFI_PASSWORD "YOUR_PASSWORD"

// --- ENDPOINT OPTIONS ---
// Use MQTT or HTTP — enable only ONE

// MQTT Settings
#define USE_MQTT true
#define MQTT_SERVER "192.168.1.20"
#define MQTT_PORT 1883
#define MQTT_TOPIC "clean_air/sensor/node_01"

// HTTP Settings
#define USE_HTTP false
#define API_ENDPOINT "https://yourserver.com/api/airdata"

// --- SENSOR SETTINGS ---
#define PMS_RX 16
#define PMS_TX 17
#define BME280_I2C_ADDR 0x76

// Transmission interval (ms)
#define SEND_INTERVAL 5000

#endif
