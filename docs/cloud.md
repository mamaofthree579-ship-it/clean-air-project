`markdown
# Cloud Integration

Nodes submit data via HTTPS REST API.

---

## Payload Format

```json
{
  "device_id": "abc123",
  "pm25": 11,
  "pm10": 22,
  "temp": 23.1,
  "humidity": 55.0,
  "voc": 120
}
