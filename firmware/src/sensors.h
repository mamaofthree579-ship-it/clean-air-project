#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>

struct SensorReadings {
  int pm1_0;
  int pm2_5;
  int pm10;
  float temperature;
  float humidity;
  int voc_index; // optional
};

// Initialize all sensors (UART PMS5003, I2C BME280, optional VOC)
void initSensors();

// Read sensors and return struct
SensorReadings readAllSensors();

#endif
