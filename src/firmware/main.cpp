#include <Arduino.h>
#include "config.h"
#include <WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>
#include "PMS.h"
#include "Adafruit_BME280.h"

// --- Global Objects ---
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);
PMS pms(Serial2);
PMS::DATA pmsData;
Adafruit_BME280 bme;

// --- WiFi ---
void connectWiFi() {
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to WiFi");
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi connected.");
}

// --- MQTT ---
void connectMQTT() {
    mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
    while (!mqttClient.connected()) {
        mqttClient.connect("CleanAirNode");
        delay(500);
    }
}

// --- Setup ---
void setup() {
    Serial.begin(115200);
    Serial2.begin(9600, SERIAL_8N1, PMS_RX, PMS_TX);

    connectWiFi();

    if (USE_MQTT) connectMQTT();

    bool status = bme.begin(BME280_I2C_ADDR);
    Serial.println(status ? "BME OK" : "BME FAIL");
}

// --- Loop ---
void loop() {
    if (USE_MQTT && !mqttClient.connected()) connectMQTT();
    mqttClient.loop();

    if (pms.read(pmsData)) {
        float temp = bme.readTemperature();
        float hum = bme.readHumidity();

        // Build JSON payload
        String payload = "{";
        payload += "\"pm25\":" + String(pmsData.PM_AE_UG_2_5) + ",";
        payload += "\"pm10\":" + String(pmsData.PM_AE_UG_10_0) + ",";
        payload += "\"temp\":" + String(temp) + ",";
        payload += "\"humidity\":" + String(hum);
        payload += "}";

        // MQTT
        if (USE_MQTT) {
            mqttClient.publish(MQTT_TOPIC, payload.c_str());
        }

        // HTTP
        if (USE_HTTP) {
            WiFiClient client;
            if (client.connect(API_ENDPOINT, 443)) {
                client.print(String("POST ") + API_ENDPOINT + " HTTP/1.1\r\n");
                client.println("Content-Type: application/json");
                client.println("Connection: close");
                client.println();
                client.print(payload);
            }
        }

        delay(SEND_INTERVAL);
    }
}
