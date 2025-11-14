#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>

struct SensorData {
    int pm1_0;
    int pm2_5;
    int pm10;
};

void initSensors();
SensorData readPMS();

#endif
