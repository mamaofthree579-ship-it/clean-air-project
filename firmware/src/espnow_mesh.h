#ifndef ESPNOW_MESH_H
#define ESPNOW_MESH_H

void espnowInit();
bool espnowSend(const uint8_t* peerMac, const uint8_t* data, size_t len);

#endif
