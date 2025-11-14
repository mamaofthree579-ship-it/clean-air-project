#include "ota.h"
#include <Arduino.h>
#include <WiFi.h>
#include <ArduinoOTA.h>

void setupOTA(const char* hostname) {
    ArduinoOTA.setHostname(hostname);
    ArduinoOTA.onStart([]() {
        Serial.println("[OTA] Start");
    });
    ArduinoOTA.onEnd([]() {
        Serial.println("\n[OTA] End");
    });
    ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
        Serial.printf("[OTA] Progress: %u%%\r", (progress / (total / 100)));
    });
    ArduinoOTA.onError([](ota_error_t error) {
        Serial.printf("[OTA] Error[%u]\n", error);
    });
    ArduinoOTA.begin();
    Serial.println("[OTA] Ready");
}
