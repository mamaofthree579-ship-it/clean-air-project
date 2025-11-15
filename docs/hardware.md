`markdown
# Hardware Overview

This section describes the sensors, wiring, and recommended build process.

---

## Core Components

| Sensor | Purpose | Protocol |
|-------|---------|-----------|
| PMS7003 | PM1/2.5/10 | UART |
| BME280 | Temperature & Humidity | I2C |
| SGP30 (optional) | VOC eCO2 | I2C |
| NEO-6M GPS (optional) | Location | UART |

---

## Wiring

See the full wiring guide in the schematics section.

- PMS7003 → UART RX/TX  
- BME280 → I2C SDA/SCL  
- SGP30 → I2C SDA/SCL  
- ESP32 → 5V/3.3V regulator  

---

## Enclosure

Recommended:
- Laser-cut acrylic
- Weather-resistant vents
- PM sensor intake separated from electronics
- 
