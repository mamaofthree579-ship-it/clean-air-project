#include <Arduino.h>
#include "config.h"
#include "sensors.h"
#include "network.h"
#include "utilities.h"

unsigned long lastSensorRead = 0;
unsigned long lastUpload = 0;

SensorReadings latest = {0};

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("\n=== Clean Air Node Boot ===");

  initLED();
  flashLED(2, 80);

  initSensors();        // sensor init (PMS, BME, optional VOC)
  initNetwork();        // WiFi init (and MQTT / OTA optional)

  flashLED(3, 50);
}

void loop() {
  unsigned long now = millis();

  if (now - lastSensorRead >= SENSOR_READ_MS) {
    lastSensorRead = now;
    latest = readAllSensors();
    Serial.println("[SENSOR] Read complete");
  }

  if (now - lastUpload >= UPLOAD_INTERVAL_MS) {
    lastUpload = now;
    Serial.println("[UPLOAD] Sending data");
    bool ok = sendData(latest);
    if (ok) {
      flashLED(1, 60);
      Serial.println("[UPLOAD] Success");
    } else {
      Serial.println("[UPLOAD] Failed");
      flashLED(2, 120);
    }
  }

  // Optional: handle OTA
  #if ENABLE_OTA
  handleOTA();
  #endif

  delay(50);
}
