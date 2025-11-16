from fastapi import FastAPI, File, UploadFile, HTTPException
import os, json
app = FastAPI()

UPLOAD_DIR = "api/ota_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/ota/upload/{device_id}")
async def upload_firmware(device_id: str, file: UploadFile = File(...), version: str = "1.0.0"):
    filename = f"{device_id}-{version}.bin"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)
    # create manifest
    manifest = {
        "device_id": device_id,
        "version": version,
        "url": f"/api/ota/files/{filename}",
        "sha256": "",  # optionally compute
        "notes": ""
    }
    with open(os.path.join(UPLOAD_DIR, f"{device_id}-{version}.json"), "w") as mf:
        json.dump(manifest, mf)
    return {"ok": True, "manifest": manifest}

@app.get("/api/ota/manifest/{device_id}")
def get_manifest(device_id: str):
    # return latest manifest for device_id by lexicographic sort (simple)
    files = [f for f in os.listdir(UPLOAD_DIR) if f.startswith(device_id) and f.endswith(".json")]
    if not files:
        raise HTTPException(404, "No manifest")
    latest = sorted(files)[-1]
    with open(os.path.join(UPLOAD_DIR, latest)) as fh:
        return json.load(fh)

@app.get("/api/ota/files/{filename}")
def download_file(filename: str):
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(404, "Not found")
    return fastapi.responses.FileResponse(path, media_type="application/octet-stream", filename=filename)

Notes

Device firmware periodically GETs /api/ota/manifest/<device_id>, compares version, downloads url if newer.

For production, host OTA files on CDN/HTTPS, compute sha256, sign manifests.
