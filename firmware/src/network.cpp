#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "network.h"
#include "config.h"
#include "sensors.h"

void connectWiFi() {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to WiFi");

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    
    Serial.println("\nWiFi connected!");
}

void sendPayload() {
    if (WiFi.status() != WL_CONNECTED) return;

    SensorData data = readPMS();

    JsonDocument doc;
    doc["device_id"] = DEVICE_ID;
    doc["pm1_0"] = data.pm1_0;
    doc["pm2_5"] = data.pm2_5;
    doc["pm10"] = data.pm10;

    String payload;
    serializeJson(doc, payload);

    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");

    int code = http.POST(payload);
    http.end();

    Serial.printf("POST %d\n", code);
}
