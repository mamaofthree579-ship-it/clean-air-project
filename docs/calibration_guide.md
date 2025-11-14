Calibration Guide

Calibration improves accuracy for PM, temperature, humidity, and VOC values.

---

## 1. PM Sensor Calibration

**Not user-modifiable**  
Plantower sensors contain factory calibration.

Recommended:  
- Warm up sensor for 30–60 seconds  
- Apply optional smoothing (moving average 5–15 samples)

---

## 2. Temperature & Humidity Calibration

If using BME280, apply:

temp_corrected = temp_raw - enclosure_bias_temp humidity_corrected = hum_raw - enclosure_bias_hum

Typical biases:  
- Temperature offset: **+2°C to +5°C inside enclosure**  
- Humidity offset: **+3% to +6%**

---

## 3. VOC Sensor Calibration (CCS811/SGP30)

- Allow 20–30 minutes for baseline burn-in  
- Store baseline values to EEPROM  
- Restore baseline on reboot  

---

## 4. Cross-Calibration

Optional but recommended:

Compare your node with:

- Nearby government stations  
- PurpleAir or Clarity monitors  
- Adjacent Clean Air Project nodes  

Then adjust:

calibrated_pm = (raw_pm * slope) + intercept

