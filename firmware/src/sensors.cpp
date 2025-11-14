#include "sensors.h"
#include "config.h"

HardwareSerial pmsSerial(2); // UART2 on ESP32

SensorData readPMS() {
    SensorData data = {0, 0, 0};

    pmsSerial.begin(9600, SERIAL_8N1, PMS_RX, PMS_TX);

    if (pmsSerial.available() > 0) {
        if (pmsSerial.read() == 0x42) {
            if (pmsSerial.read() == 0x4D) {
                uint8_t buffer[30];
                pmsSerial.readBytes(buffer, 30);

                data.pm1_0 = (buffer[4] << 8) | buffer[5];
                data.pm2_5 = (buffer[6] << 8) | buffer[7];
                data.pm10  = (buffer[8] << 8) | buffer[9];
            }
        }
    }

    return data;
}
