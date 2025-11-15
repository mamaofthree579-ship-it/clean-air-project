Getting Started

This guide walks you through assembling, flashing, and deploying a Clean Air Community Node.

---

## Requirements

### Hardware
- ESP32 Dev Module  
- PMS7003 particulate sensor  
- BME280 temp/humidity sensor  
- Optional: SGP30 VOC sensor  
- Optional: CO₂ sensor  
- Power supply (USB or renewable module)

### Software
- PlatformIO  
- Python 3.9+  
- USB-to-Serial drivers  

---

## Steps

### 1. Clone the repository

```bash
git clone https://github.com/USERNAME/clean-air-node
cd clean-air-node

2. Install dependencies

pip install -r requirements.txt

3. Build firmware

pio run

4. Upload firmware

pio run --target upload

5. View serial logs

pio device monitor


---

Next Steps

Configure WiFi and API keys in src/config.h

Mount hardware into enclosure

Deploy the node on site
