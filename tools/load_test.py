#!/usr/bin/env python3
# tools/load_test.py
import requests, time, random, json
from datetime import datetime

API = "https://YOUR_API_URL_HERE/api/data"
RPS = 5   # requests per second
DURATION = 60  # seconds

def gen_payload(i):
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "device_id": f"loadtest-{i%10}",
        "pm25": round(random.uniform(1,80),1),
        "temperature": round(random.uniform(15,30),1),
        "humidity": round(random.uniform(20,80),1),
        "lat": 37.77 + random.uniform(-0.02,0.02),
        "lon": -122.42 + random.uniform(-0.02,0.02)
    }

def run():
    start = time.time()
    sent = 0
    while time.time() - start < DURATION:
        t0 = time.time()
        for i in range(RPS):
            payload = gen_payload(sent+i)
            try:
                r = requests.post(API, json=payload, timeout=3)
                print(r.status_code, r.text[:100])
            except Exception as e:
                print("ERR", e)
        sent += RPS
        # sleep until next second
        dt = 1 - (time.time() - t0)
        if dt > 0:
            time.sleep(dt)

if __name__ == "__main__":
    run()

How to use

pip install requests
python tools/load_test.py

Adjust RPS and DURATION to model your expected load.
