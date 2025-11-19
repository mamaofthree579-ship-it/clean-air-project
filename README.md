## Clean Air Project — Community Air Quality Monitoring Network

The Clean Air Project is an open-source initiative that enables communities to deploy low-cost, high-accuracy air quality monitoring nodes. The system collects, processes, and shares real-time PM2.5, PM10, temperature, humidity, and VOC data.

This repository provides:

- Hardware build guides  
- Wiring schematics  
- Sensor calibration instructions  
- Firmware source templates  
- Cloud/server integration patterns  
- Community training materials  
- Logo and branding assets  

---

## Features

- 🟢 **Modular Node Design** — ESP32-based microcontroller with swappable sensors  
- 📡 **Multi-Path Communications** — Wi-Fi, LoRaWAN (optional), offline data buffering  
- 📊 **Data Processing** — On-node smoothing, calibration, and timestamped batching  
- 🌐 **Open API** — REST + MQTT ingestion formats  
- 🧩 **Easy Assembly** — Beginner-friendly build & wiring guides  
- 🌱 **Community-Driven** — Designed for teachers, local groups, and researchers  

---

## Repository Structure

. ├── README.md ├── docs/ │   ├── build_guide.md │   ├── wiring_guide.md │   ├── calibration_guide.md │   ├── contributing.md │   ├── api_reference.md ├── firmware/ │   ├── src_template/ │   │   ├── main.cpp │   │   ├── config.h │   │   ├── sensors.cpp │   │   ├── sensors.h │   │   ├── network.cpp │   │   ├── network.h │   └── platformio.ini ├── branding/ │   ├── logos/ │   ├── style_guide.md ├── training/ │   ├── workshop_instructor_guide.md │   ├── workshop_slides_overview.md ├── tests/ │   ├── test_plan.md └── translations/ ├── template_en.md

---

## License

This project is released under the **MIT License**. Contributions welcome!

---

## How to Contribute

See: `docs/contributing.md`

---

## Contact

Questions? Want to join the community?  
Open an Issue or email the maintainers.
│   ├── maintenance.md
│   ├── community_rollout.md
│   ├── faq.md
│   └── schematics.md
│
├── hardware/
│   ├── schematics/
│   │   └── *.png
│   └── bom/
│       └── bill_of_materials.csv
│
├── src/
│   ├── firmware/
│   │   ├── config.h
│   │   ├── main.cpp
│   │   └── libraries/
│   └── dashboard/
│       ├── api/
│       └── frontend/
│
├── LICENSE
└── README.md
```

---

# 🛠 What You Can Build

### 1️⃣ Community Air Sensor Node
- PM1.0 / PM2.5 / PM10  
- Temperature & humidity  
- Optional VOC  
- Wi-Fi connected  
- Pushes data to dashboards or local servers  

### 2️⃣ DIY Air Purifier
- Based on Corsi-Rosenthal box  
- Uses high-grade MERV filters  
- Low-cost and highly effective  
- Optional carbon filtration  

---

# 🚀 Quick Start

### Build the hardware  
See:  
`docs/build_guide.md`

### Wire everything  
See:  
`docs/wiring_guide.md`

### Flash the firmware  
See:  
`docs/firmware_setup.md`

### Deploy in your community  
See:  
`docs/community_rollout.md`

---

# 🔧 Contributions
All PRs welcome.  
Community labs, universities, schools, and environmental justice groups are especially encouraged to join.

---

# 📄 License
MIT License — free to use, modify, distribute.

---

# 🌍 Together we build cleaner air.
