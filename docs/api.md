`markdown
# API Reference

## POST /api/v1/submit

Submit a JSON payload.

### Body:
- pm1
- pm25
- pm10
- temperature
- humidity
- voc
- device_id

### Response:
```json
{"status":"ok"}


---

GET /api/v1/device/{id}

Returns registered device info.
