API Reference — Clean Air Project

This document defines the data formats used for cloud ingestion.

---

## REST Endpoint

POST /api/v1/ingest Content-Type: application/json

### JSON Body
```json
{
  "device_id": "node-001",
  "timestamp": 1712345678,
  "pm25": 8.42,
  "pm10": 12.77,
  "temperature": 21.4,
  "humidity": 44.1,
  "voc_index": 13,
  "battery": 4.91
}


---

MQTT Topics

clean_air/<device_id>/data
clean_air/<device_id>/status
clean_air/<device_id>/config


---

Responses

200 OK

{ "status": "accepted" }

400 Bad Request

{ "error": "missing fields" }

---

## **docs/contributing.md**
*(requested earlier, included again for completeness)*  
```markdown
# Contributing Guide

Thank you for contributing to the Clean Air Project!

---

## How to Participate

1. Fork the repository  
2. Create a feature branch  
3. Submit a pull request  
4. Join discussion in Issues  

---

## Coding Standards

- Keep firmware code portable  
- Use descriptive variable names  
- Add comments for hardware behavior  
- Follow existing formatting patterns  

---

## Documentation Requirements

All major PRs should include:

- Updated docs in `/docs/`  
- Wiring or schematic changes  
- New diagrams if needed  

---

## Reporting Issues

Use the *Issue Template*:

- Describe the problem  
- Steps to reproduce  
- Expected behavior  
- Screenshot or logs
