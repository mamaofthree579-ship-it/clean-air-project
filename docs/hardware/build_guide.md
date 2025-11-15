# Clean Air Project — Build Guide
A simple, step-by-step guide to assemble the Community Air Sensor Node and the DIY Air Purifier Unit. Designed for beginners, community groups, and schools.

---

## 📦 Required Materials

### 🔹 Electronics (Sensor Node)
- ESP32 or ESP8266 microcontroller  
- Plantower PMS5003 or SDS011 particulate sensor  
- SHT31 or BME280 temperature/humidity sensor  
- MQ-135 or SGP30 gas/VOC sensor (optional)  
- 5V power supply or USB power bank  
- Wires (female–female dupont)  
- Small enclosure  

### 🔹 Air Purifier Unit (DIY)
- 20" box fan *or* 120mm PC fan array  
- MERV-13, 14, or 16 filter (20"x20")  
- Cardboard or rigid foam board  
- Duct tape or weatherstripping tape  
- Optional: activated carbon sheet  

---

## 🛠 Tools Needed
- Small screwdriver  
- Scissors or utility knife  
- Hot glue gun (optional)  
- Tape  

---

# 1️⃣ Build the Community Air Sensor Node

## Step 1 — Unpack Components
Remove sensors from packaging. Ensure cable lengths reach the ESP32 board.

---

## Step 2 — Connect the PMS Particle Sensor
Use the 5-pin JST cable.

| PMS Pin | ESP32 Pin |
|---------|-----------|
| 5V      | 5V        |
| GND     | GND       |
| TX      | RX        |
| RX      | TX        |

---

## Step 3 — Connect the Temperature/Humidity Sensor
(BME280 or SHT31)

| BME/SHT Pin | ESP32 Pin |
|-------------|-----------|
| VIN         | 3.3V      |
| GND         | GND       |
| SDA         | D21       |
| SCL         | D22       |

---

## Step 4 — Connect Optional Gas/VOC Sensor
(MQ-135 or SGP30)

| VOC Pin | ESP32 Pin |
|---------|-----------|
| VIN     | 5V or 3.3V |
| GND     | GND       |
| AOUT/I2C | A0 or SDA/SCL |

---

## Step 5 — Mount Components
- Tape or screw sensors inside enclosure  
- Cut vent holes for airflow  
- Add a small mesh to keep dust out  

---

## Step 6 — Power Up & Flash Firmware
Use USB cable to upload firmware (from `src/firmware/` in the repo).  
Verify Wi-Fi connection.

---

# 2️⃣ Build the DIY Air Purifier ("Corsi-Rosenthal" Style)

## Step 1 — Place Fan Face-Down
Airflow direction must blow **away** from the filter.

---

## Step 2 — Seal Filter to Fan
Use tape to attach a MERV-13+ filter to the fan housing.

Ensure:
- No gaps  
- Arrow on filter points **toward the fan**  

---

## Step 3 — Add Stabilizer Shroud (Optional)
A cardboard ring improves efficiency by ~10–20%.

Cut a ring and tape it around fan exhaust.

---

## Step 4 — Add Carbon Layer (Optional)
Tape carbon sheet on intake side for VOC reduction.

---

## Step 5 — Power & Safety
- Do not leave unattended  
- Replace filter every 3–4 months  
- Label with date installed  

---

# 🎉 Build Complete!
You now have a fully operational **sensor node** and/or **DIY purifier** for community clean-air networks.
