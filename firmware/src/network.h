#ifndef NETWORK_H
#define NETWORK_H

#include <Arduino.h>
#include "sensors.h"

void connectWiFi();
void sendPayload(SensorData data);

#endif
