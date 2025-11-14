ifndef CONFIG_H
#define CONFIG_H

// WiFi credentials (best overridden using build flags or secrets.h)
#define WIFI_SSID     "YOUR_WIFI"
#define WIFI_PASS     "YOUR_PASS"

// Device identity
#define DEVICE_ID     "node-001"

// API Endpoint
#define API_URL       "https://your-server.com/api/v1/ingest"

// GPIO Pins
#define PMS_RX 16
#define PMS_TX 17
#define I2C_SDA 21
#define I2C_SCL 22

// Send interval (milliseconds)
#define SEND_INTERVAL 30000

// Debug mode
#define DEBUG true

#endif
