#include "sensors.h"
#include <Wire.h>
#include <Adafruit_BME280.h>
#include <SparkFunCCS811.h>
#include <SoftwareSerial.h>

// PMS
SoftwareSerial pmsSerial(PMS_RX, PMS_TX);

// BME280
Adafruit_BME280 bme;

// CCS811
CCS811 voc;

// Values
float pm25 = 0;
float pm10 = 0;
float temperature = 0;
float humidity = 0;
int vocIndex = -1;

void setupSensors() {
    // PMS
    pmsSerial.begin(9600);

    // BME280
    if (!bme.begin(0x76)) {
        Serial.println("[ERR] BME280 not found!");
    }

    // CCS811
    if (!voc.begin()) {
        Serial.println("[ERR] VOC sensor not found!");
    }
}

void readSensors() {
    // PMS frame parsing (simplified)
    if (pmsSerial.available() > 32) {
        uint8_t buffer[32];
        pmsSerial.readBytes(buffer, 32);

        pm25 = (buffer[12] << 8) | buffer[13];
        pm10 = (buffer[14] << 8) | buffer[15];
    }

    // BME280
    temperature = bme.readTemperature();
    humidity = bme.readHumidity();

    // VOC
    if (voc.dataAvailable()) {
        voc.readAlgorithmResults();
        vocIndex = voc.getTVOC();
    }
}
