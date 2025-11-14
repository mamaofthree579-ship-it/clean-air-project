#include "network.h"
#include "config.h"
#include "utilities.h"

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

void connectWiFi() {
    Serial.printf("Connecting to WiFi: %s\n", WIFI_SSID);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    int retries = 0;
    flashLED(5, 50);

    while (WiFi.status() != WL_CONNECTED && retries < 30) {
        delay(300);
        Serial.print(".");
        retries++;
    }

    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\nWiFi connected!");
    } else {
        Serial.println("\nWiFi connection failed!");
    }
}

void sendPayload(SensorData data) {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi disconnected — retrying connection...");
        connectWiFi();
        return;
    }

    JsonDocument doc;
    doc["device_id"] = DEVICE_ID;
    doc["pm1_0"] = data.pm1_0;
    doc["pm2_5"] = data.pm2_5;
    doc["pm10"]  = data.pm10;

    String payload;
    serializeJson(doc, payload);

    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");

    Serial.println("Sending payload...");
    int code = http.POST(payload);

    Serial.printf("Server response: %d\n", code);
    http.end();

    // Success feedback
    if (code == 200 || code == 201) {
        flashLED(2, 80);
    } else {
        flashLED(5, 80);
    }
}

