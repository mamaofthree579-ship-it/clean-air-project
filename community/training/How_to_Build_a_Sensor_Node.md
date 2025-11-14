How to Build a Clean Air Sensor Node

## 🧰 Tools Needed  
- Small Phillips screwdriver  
- Micro USB cable  
- Wire cutters / Zip ties  
- Laptop with USB port  

---

## 🛠 Step 1 — Connect Sensors  
1. Plug PMS5003 into JST connector  
2. Connect BME280 to ESP32 I2C pins  
3. Secure sensors inside enclosure  

---

## ⚙️ Step 2 — Flash Firmware  
1. Install PlatformIO  
2. Connect ESP32  
3. Run: `pio run --target upload`  
4. Sensor auto-connects to WiFi  

---

## 📶 Step 3 — Verify Data  
- Open dashboard  
- Look for “Node Online” status  
- Confirm PM2.5/PM10/Temp/Humidity values  

---

## 🎉 You're Done!  
You now have a working Clean Air Node.
