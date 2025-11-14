#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "config.h"
#include "sensors.h"
#include "network.h"

unsigned long lastSend = 0;

void setup() {
    Serial.begin(115200);
    delay(200);

    if (DEBUG) Serial.println("[BOOT] Starting Clean Air Project Node...");

    setupSensors();
    setupNetwork();
}

void loop() {
    readSensors();

    unsigned long now = millis();
    if (now - lastSend >= SEND_INTERVAL) {
        if (DEBUG) Serial.println("[LOOP] Sending payload...");
        sendPayload();
        lastSend = now;
    }
}
