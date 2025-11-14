#ifndef CONFIG_H
#define CONFIG_H

// ------- EDIT THESE -------
#define WIFI_SSID     "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

#define DEVICE_ID     "airnode-001"
#define API_URL       "https://example.com/api/v1/ingest"

// Choose transport: set to 1 to enable
#define ENABLE_HTTP   1
#define ENABLE_MQTT   0
#define ENABLE_OTA    0

// MQTT settings (if ENABLE_MQTT)
#define MQTT_BROKER   "mqtt.example.com"
#define MQTT_PORT     1883
#define MQTT_TOPIC    "clean_air/data"

// Timing
#define SENSOR_READ_MS     15 * 1000   // read sensors every 15s
#define UPLOAD_INTERVAL_MS 60 * 1000   // upload every 60s

// Pins (ESP32 default)
#define PMS_RX 16
#define PMS_TX 17
#define I2C_SDA 21
#define I2C_SCL 22
#define LED_PIN 2

#endif // CONFIG_H
