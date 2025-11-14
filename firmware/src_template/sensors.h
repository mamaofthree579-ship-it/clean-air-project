#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>

extern float pm25, pm10;
extern float temperature, humidity;
extern int vocIndex;

void setupSensors();
void readSensors();

#endif
