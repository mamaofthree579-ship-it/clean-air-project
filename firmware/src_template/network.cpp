#include "network.h"
#include "config.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "sensors.h"

void setupNetwork() {
    WiFi.begin(WIFI_SSID, WIFI_PASS);

    Serial.print("[NET] Connecting");
    while (WiFi.status() != WL_CONNECTED) {
        delay(400);
        Serial.print(".");
    }
    Serial.println("\n[NET] Connected!");
}

void sendPayload() {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("[ERR] WiFi disconnected.");
        return;
    }

    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<256> doc;
    doc["device_id"] = DEVICE_ID;
    doc["pm25"] = pm25;
    doc["pm10"] = pm10;
    doc["temperature"] = temperature;
    doc["humidity"] = humidity;
    doc["voc_index"] = vocIndex;
    doc["timestamp"] = (unsigned long)(millis()/1000);

    String jsonStr;
    serializeJson(doc, jsonStr);

    int code = http.POST(jsonStr);
    Serial.printf("[NET] POST code: %d\n", code);

    http.end();
}
