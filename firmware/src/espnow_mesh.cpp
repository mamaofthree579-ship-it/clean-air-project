#include "espnow_mesh.h"
#include <WiFi.h>
#include <esp_now.h>
#include <Arduino.h>

void OnDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
    Serial.print("[ESPNOW] Received from ");
    for (int i=0;i<6;i++) { Serial.printf("%02X:", mac[i]); }
    Serial.printf(" len=%d\n", len);
}

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
    Serial.print("[ESPNOW] Sent status: ");
    Serial.println(status == ESP_NOW_SEND_SUCCESS ? "OK" : "Fail");
}

void espnowInit() {
    WiFi.mode(WIFI_STA);
    if (esp_now_init() != ESP_OK) {
        Serial.println("[ESPNOW] init failed");
        return;
    }
    esp_now_register_recv_cb(OnDataRecv);
    esp_now_register_send_cb(OnDataSent);
    Serial.println("[ESPNOW] Initialized");
}

bool espnowSend(const uint8_t* peerMac, const uint8_t* data, size_t len) {
    esp_err_t res = esp_now_send(peerMac, data, len);
    return res == ESP_OK;
}
