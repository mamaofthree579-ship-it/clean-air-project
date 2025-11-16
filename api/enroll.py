from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3, secrets, os

DB = os.path.join("api", "devices.db")
os.makedirs("api", exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

conn = get_conn()
conn.execute("""CREATE TABLE IF NOT EXISTS devices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  device_id TEXT UNIQUE,
  token TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  metadata TEXT
)""")
conn.commit()

app = FastAPI(title="CleanAir Enrollment")

class EnrollReq(BaseModel):
    device_id: str
    metadata: dict = {}

@app.post("/api/enroll")
def enroll(req: EnrollReq):
    token = secrets.token_urlsafe(24)
    try:
        conn.execute("INSERT INTO devices (device_id, token, metadata) VALUES (?, ?, ?)",
                     (req.device_id, token, json.dumps(req.metadata)))
        conn.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"device_id": req.device_id, "token": token}

@app.get("/api/devices")
def list_devices():
    cur = conn.execute("SELECT device_id, token, created_at, metadata FROM devices")
    rows = [dict(r) for r in cur.fetchall()]
    return rows

How to run locally

pip install fastapi "uvicorn[standard]"
uvicorn api.enroll:app --reload --port 8001

Usage

POST /api/enroll with JSON {"device_id":"node-001"} returns token to provision into device config.

GET /api/devices lists registered devices.


(If you want, I can add authentication for the admin endpoints.)
