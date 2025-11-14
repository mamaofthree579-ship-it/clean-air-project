# PMS5003 Troubleshooting & Best Practices

## Symptoms & Fixes

### 1. No output / sensor silent
- Ensure sensor gets 5V (PMS commonly needs 5V). Check cable polarity.
- Check RX/TX wiring (swap if no output).
- Confirm serial port speed (9600) and UART pins used match firmware.

### 2. Unstable or garbage data
- Ensure correct byte framing and full read of 32-byte frame. Use hardware serial if possible (SoftwareSerial unstable on ESP32).
- Confirm buffer reads exactly 32 bytes and validate start bytes `0x42 0x4d`.
- Check for noisy power — add small decoupling capacitor (100 uF) on 5V line.

### 3. Very high PM readings (false positives)
- Check for local sources (boiling water, incense); run baseline in clean air.
- Ensure sensor inlet not blocked and not too close to fan exhaust.
- Move sensor further away from humid soil or mist — humidity can register as particulates.
- Add micro-mesh moisture shield and advanced humidity compensation.

### 4. Slow wake or intermittent responses
- Some PMS models have sleep pin; ensure it's not held low. Check datasheet's `SET` pin.
- Provide continuous power during testing.

### 5. Calibration drift vs reference monitors
- PMS are low-cost optical sensors; consider using linear correction against a nearby reference (government or research-grade station).
- Use a 24–72 hour co-location to calculate slope/intercept: `calibrated = raw * slope + intercept`.

## Best Practices
- Use hardware UART (HardwareSerial) on ESP32 for reliable reads.
- Warm-up sensor for at least 30 seconds after power-on.
- Protect sensor from dust and insects with a fine mesh; avoid covering inlet.
- Keep I2C and UART wiring separate if possible to reduce interference.

## Example: Validate Frame Parsing (pseudo)
1. Read 2 bytes — check `0x42 0x4D`.
2. Read next 30 bytes into buffer.
3. Compute checksum (last two bytes) and compare.
4. Extract PM values at indices per datasheet.
5. 
