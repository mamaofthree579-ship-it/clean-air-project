#include <Arduino.h>
#include "config.h"
#include "sensors.h"
#include "network.h"
#include "utilities.h"

unsigned long lastSend = 0;
const unsigned long sendInterval = 30 * 1000; // 30 seconds

void setup() {
    Serial.begin(115200);
    delay(500);

    Serial.println("\n--- CLEAN AIR PROJECT: ESP32 AIR NODE ---");

    initLED();
    flashLED(3, 150);

    connectWiFi();
    initSensors();
}

void loop() {
    if (millis() - lastSend > sendInterval) {
        lastSend = millis();

        SensorData data = readPMS();

        Serial.println("--- Sensor Reading ---");
        Serial.printf("PM1.0: %d\n", data.pm1_0);
        Serial.printf("PM2.5: %d\n", data.pm2_5);
        Serial.printf("PM10:  %d\n", data.pm10);

        flashLED(1, 50);
        sendPayload(data);
    }

    delay(50);
}
