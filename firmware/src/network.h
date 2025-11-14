#ifndef NETWORK_H
#define NETWORK_H

#include "sensors.h"

void initNetwork();
bool sendData(const SensorReadings &s);

#if ENABLE_OTA
void setupOTA();
#endif

#endif
