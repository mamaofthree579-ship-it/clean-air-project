# Clean Air Project API Server Template (Flask)

from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)
DATABASE = "data.jsonl"

@app.post("/upload")
def upload():
    data = request.json
    data["timestamp"] = datetime.datetime.utcnow().isoformat()

    with open(DATABASE, "a") as f:
        f.write(f"{data}\n")

    return jsonify({"status": "ok"}), 200

@app.get("/data")
def data():
    with open(DATABASE) as f:
        lines = [eval(l) for l in f.readlines()]
    return jsonify(lines)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
  
