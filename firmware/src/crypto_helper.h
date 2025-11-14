#ifndef CRYPTO_HELPER_H
#define CRYPTO_HELPER_H

#include <Arduino.h>

String hmac_sha256_base64(const String& payload, const String& secret);

#endif
