#include "sensors.h"
#include "config.h"
#include <Wire.h>
#include <Adafruit_BME280.h>
#include <SparkFunCCS811.h>
#include <HardwareSerial.h>

HardwareSerial pmsSerial(2); // UART2 for PMS
Adafruit_BME280 bme;
CCS811 voc;

void initSensors() {
  // PMS UART
  pmsSerial.begin(9600, SERIAL_8N1, PMS_RX, PMS_TX);
  delay(200);

  // BME280
  Wire.begin(I2C_SDA, I2C_SCL);
  if (!bme.begin(0x76)) {
    Serial.println("[WARN] BME280 not found at 0x76, trying 0x77");
    if (!bme.begin(0x77)) {
      Serial.println("[ERROR] BME280 not detected");
    }
  }

  // VOC sensor (optional)
  if (voc.begin()) {
    Serial.println("[INFO] VOC sensor initialized");
  } else {
    Serial.println("[WARN] VOC sensor not found or init failed");
  }
}

// Helper: read PMS5003 frame if available
static bool readPMSFrame(int &pm1, int &pm25, int &pm10) {
  if (!pmsSerial.available()) return false;

  // Look for 0x42 0x4D
  if (pmsSerial.read() != 0x42) return false;
  if (pmsSerial.read() != 0x4D) return false;

  uint8_t buf[30];
  if (pmsSerial.readBytes(buf, 30) != 30) return false;

  pm1  = (buf[4] << 8) | buf[5];
  pm25 = (buf[6] << 8) | buf[7];
  pm10 = (buf[8] << 8) | buf[9];

  // TODO: validate checksum using buf[28..29]
  return true;
}

SensorReadings readAllSensors() {
  SensorReadings r = {0,0,0,0.0f,0.0f,-1};

  // Read PMS (try multiple bytes if needed)
  int pm1=0, pm25=0, pm10=0;
  if (readPMSFrame(pm1, pm25, pm10)) {
    r.pm1_0 = pm1;
    r.pm2_5 = pm25;
    r.pm10 = pm10;
  } else {
    // no frame available -> leave zeros
  }

  // BME280
  r.temperature = bme.readTemperature();
  r.humidity = bme.readHumidity();

  // VOC (if available)
  if (voc.dataAvailable()) {
    voc.readAlgorithmResults();
    r.voc_index = voc.getTVOC();
  }

  return r;
}
