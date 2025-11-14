#include "lora_lmic.h"
#include <lmic.h>
#include <hal/hal.h>
#include <SPI.h>

// Example placeholder OTAA keys (REPLACE with real keys)
static const u1_t PROGMEM APPEUI[8] = { 0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08 };
static const u1_t PROGMEM DEVEUI[8] = { 0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17 };
static const u1_t PROGMEM APPKEY[16] = { 0x20,0x21,0x22,0x23,0x24,0x25,0x26,0x27,0x28,0x29,0x2A,0x2B,0x2C,0x2D,0x2E,0x2F };

void os_getArtEui (u1_t* buf) { memcpy_P(buf, APPEUI, 8); }
void os_getDevEui (u1_t* buf) { memcpy_P(buf, DEVEUI, 8); }
void os_getDevKey (u1_t* buf) { memcpy_P(buf, APPKEY, 16); }

static void onEvent (ev_t ev) {
    Serial.print("[LMIC] Event: ");
    Serial.println(ev);
}

void loraInit() {
    // LMIC init
    os_init();
    LMIC_reset();
    LMIC_setClockError(1 * ERR_RATE);
    Serial.println("[LMIC] Initialized");
}

void loraSend(uint8_t* data, uint8_t len) {
    if (LMIC.opmode & OP_TXRXPEND) {
        Serial.println("[LMIC] TX busy");
        return;
    }
    // Prepare upstream data transmission at the next possible time.
    LMIC_setTxData2(1, data, len, 0);
    Serial.println("[LMIC] Packet queued");
}
