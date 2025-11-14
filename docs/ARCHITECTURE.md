# System Architecture

The Community Air Project consists of four major layers:

┌──────────────────────────────────┐ │   1. Hardware Layer              │ │   Sensors: PM2.5, VOC, CO2       │ │   MCU: ESP32                     │ │   Power: USB-C or battery        │ └──────────────────────────────────┘ ┌──────────────────────────────────┐ │   2. Firmware Layer              │ │   Arduino / ESP-IDF              │ │   Sensor drivers                 │ │   Data smoothing                 │ │   WiFi / OTA updates             │ └──────────────────────────────────┘ ┌──────────────────────────────────┐ │   3. Local Interface Layer       │ │   RGB LED indicator              │ │   Web dashboard (ESP hosted)     │ │   Calibration utilities          │ └──────────────────────────────────┘ ┌──────────────────────────────────┐ │   4. Cloud / Community Layer     │ │   Optional API integration        │ │   Open data standard              │ │   Community dashboards            │ └──────────────────────────────────┘

## Data Flow
1. Sensor samples raw data  
2. Firmware applies smoothing + temperature normalization  
3. Optional: Data uploaded to local dashboard or network  
4. Community can view, calibrate, and share findings

## Modularity
- Plug-in sensors  
- Multiple enclosure types  
- Independent firmware modules
- 
