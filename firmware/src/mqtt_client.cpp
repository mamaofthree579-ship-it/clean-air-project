#include "mqtt_client.h"
#include <WiFi.h>
#include <PubSubClient.h>

static WiFiClient netClient;
static PubSubClient client(netClient);
static String gClientId;

void mqttSetup(const char* broker, uint16_t port, const char* clientId) {
    client.setServer(broker, port);
    gClientId = clientId;
}

bool mqttEnsureConnected() {
    if (client.connected()) return true;
    if (WiFi.status() != WL_CONNECTED) return false;

    Serial.printf("[MQTT] Connecting as %s...\n", gClientId.c_str());
    if (client.connect(gClientId.c_str())) {
        Serial.println("[MQTT] Connected");
        return true;
    } else {
        Serial.printf("[MQTT] Failed: rc=%d\n", client.state());
        return false;
    }
}

bool mqttPublish(const char* topic, const char* payload) {
    if (!mqttEnsureConnected()) return false;
    return client.publish(topic, payload);
}

void mqttLoop() {
    if (!client.loop()) {
        // attempt reconnect in background (non-blocking simple approach)
        mqttEnsureConnected();
    }
}
