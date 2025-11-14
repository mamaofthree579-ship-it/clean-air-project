#include "crypto_helper.h"
#include <mbedtls/md.h>
#include <Base64.h> // PlatformIO lib: arduino-libs/Base64 or implement your own

String hmac_sha256_base64(const String& payload, const String& secret) {
    const unsigned char* key = (const unsigned char*)secret.c_str();
    const unsigned char* msg = (const unsigned char*)payload.c_str();
    unsigned char digest[32];

    mbedtls_md_context_t ctx;
    const mbedtls_md_info_t* info = mbedtls_md_info_from_type(MBEDTLS_MD_SHA256);
    mbedtls_md_init(&ctx);
    mbedtls_md_setup(&ctx, info, 1);
    mbedtls_md_hmac_starts(&ctx, key, secret.length());
    mbedtls_md_hmac_update(&ctx, msg, payload.length());
    mbedtls_md_hmac_finish(&ctx, digest);
    mbedtls_md_free(&ctx);

    // Base64 encode
    String b64 = base64::encode(digest, 32);
    return b64;
}
