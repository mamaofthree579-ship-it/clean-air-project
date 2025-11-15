"""
Simple load test for the cloud ingestion API.
"""

import json
import random
import time
import requests

API_URL = "https://your-server/ingest"

def generate_payload():
    return {
        "device_id": "TESTER",
        "pm1_0": random.uniform(1, 10),
        "pm2_5": random.uniform(1, 20),
        "pm10": random.uniform(1, 30),
        "humidity": random.uniform(20, 60),
        "temperature": random.uniform(15, 35)
    }

def run_test(iterations=100):
    for i in range(iterations):
        payload = generate_payload()
        r = requests.post(API_URL, json=payload)
        print(f"{i+1}/{iterations} → {r.status_code}")
        time.sleep(0.1)

if __name__ == "__main__":
    run_test()
  
