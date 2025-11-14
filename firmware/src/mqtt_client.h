#ifndef MQTT_CLIENT_H
#define MQTT_CLIENT_H

#include <Arduino.h>

void mqttSetup(const char* broker, uint16_t port, const char* clientId);
bool mqttPublish(const char* topic, const char* payload);
void mqttLoop();

#endif
