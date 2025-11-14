#include "network.h"
#include "config.h"
#include "utilities.h"

#include <WiFi.h>
#if ENABLE_HTTP
#include <HTTPClient.h>
#include <ArduinoJson.h>
#endif
#if ENABLE_MQTT
#include "mqtt_client.h"
#endif
#if ENABLE_OTA
#include <ArduinoOTA.h>
#endif

void initNetwork() {
  Serial.printf("[NET] Connecting to WiFi '%s'\n", WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts++ < 40) {
    delay(250);
    Serial.print(".");
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[NET] WiFi connected");
  } else {
    Serial.println("\n[NET] WiFi connection failed");
  }

  #if ENABLE_MQTT
  mqtt_setup(MQTT_BROKER, MQTT_PORT, DEVICE_ID);
  #endif

  #if ENABLE_OTA
  ArduinoOTA.setHostname(DEVICE_ID);
  ArduinoOTA.begin();
  Serial.println("[OTA] ready");
  #endif
}

bool sendData(const SensorReadings &s) {
  bool ok = false;

  #if ENABLE_HTTP
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(API_URL);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<256> doc;
    doc["device_id"] = DEVICE_ID;
    doc["pm1_0"] = s.pm1_0;
    doc["pm2_5"] = s.pm2_5;
    doc["pm10"] = s.pm10;
    doc["temperature"] = s.temperature;
    doc["humidity"] = s.humidity;
    doc["voc_index"] = s.voc_index;

    String payload;
    serializeJson(doc, payload);

    int code = http.POST(payload);
    http.end();
    ok = (code >= 200 && code < 300);
    Serial.printf("[HTTP] POST %d\n", code);
  } else {
    Serial.println("[HTTP] WiFi not connected");
  }
  #endif

  #if ENABLE_MQTT
  if (!ok) {
    // fallback to MQTT if enabled
    char msgbuf[256];
    StaticJsonDocument<256> doc2;
    doc2["device_id"] = DEVICE_ID;
    doc2["pm2_5"] = s.pm2_5;
    serializeJson(doc2, msgbuf, sizeof(msgbuf));
    ok = mqtt_publish(MQTT_TOPIC, msgbuf);
  }
  #endif

  return ok;
}
