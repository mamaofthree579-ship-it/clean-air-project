#ifndef UTILITIES_H
#define UTILITIES_H

void initLED();
void flashLED(int times, int ms);

#if ENABLE_OTA
void handleOTA();
#endif

#endif
