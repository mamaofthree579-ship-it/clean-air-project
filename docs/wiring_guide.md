# Clean Air Project — Wiring Guide
This guide provides detailed wiring diagrams, pinouts, and troubleshooting notes for all Clean Air Project hardware.

---

# 1️⃣ Sensor Node Wiring (ESP32 + PMS + BME/SHT)

## 📍 Wiring Diagram (Reference)
See image in:  
`hardware/schematics/community_air_sensor_node.png`

---

## A. PMS5003 / SDS011 Particle Sensor

### Pinout
| Sensor Pin | Function        | Connect to ESP32 |
|------------|-----------------|------------------|
| 5V         | Power           | 5V               |
| GND        | Ground          | GND              |
| TX         | Output Data     | RX (GPIO 16)     |
| RX         | Input Commands  | TX (GPIO 17)     |
| RESET      | Usually unused  | Leave unconnected|
| SET        | Sleep control   | Optional GPIO     |

### Notes
- PMS sensors require **5V** even if ESP32 is 3.3V logic.  
- UART serial uses 9600 baud by default.  

---

## B. BME280 / SHT31 Temperature & Humidity Sensor

### Typical I²C Wiring
| Sensor Pin | Connect to ESP32 |
|------------|------------------|
| VIN        | 3.3V             |
| GND        | GND              |
| SDA        | GPIO 21          |
| SCL        | GPIO 22          |

### Notes
- Keep I²C wires shorter than 30cm if possible.  
- If instability occurs, add pull-up resistors (4.7kΩ).  

---

## C. Optional VOC Sensor (SGP30 or MQ-135)

### SGP30 (I²C)
Same I²C wiring as BME280. Can share SDA/SCL.

### MQ-135 (Analog)
| MQ-135 | ESP32 |
|--------|--------|
| AOUT   | A0     |
| VCC    | 5V     |
| GND    | GND    |

---

# 2️⃣ Power System Wiring

## Recommended Power Setup
- USB 5V supply → ESP32  
- PMS sensor → **5V pin of ESP32**  
- Do NOT power PMS from 3.3V pin  

### Optional Backup Power
- 18650 battery + boost converter  
- USB power bank with auto-on function  

---

# 3️⃣ DIY Air Purifier Wiring (If Using PC Fans)

If using a **box fan**, skip — no wiring needed.

## A. Using PC Fans (12V)

### Materials
- 12V fans (120mm)  
- 12V power supply  
- DC barrel connector  
- Fan splitter or manual wiring  

### Wiring
```
12V PSU + → Fan + (red)
12V PSU – → Fan – (black)
```

Use parallel wiring for multi-fan setups.

### Optional Controls
- PWM for speed control  
- Temperature-trigger board for automatic mode  

---

# 4️⃣ Troubleshooting

### ❗ PMS sensor not reading?
- Swap RX/TX  
- Ensure 5V supply  
- Check cable orientation  

### ❗ I²C sensor not detected?
- Check SDA/SCL pins  
- Add pull-ups  
- Ensure 3.3V power  

### ❗ VOC readings drifting?
- Warm-up time needed (5–10 min)  

### ❗ ESP32 keeps rebooting?
- Power supply insufficient  
- Use 1A+ USB supply  

---

# ✔ Wiring Complete!
Your node should now be ready for firmware and testing.
