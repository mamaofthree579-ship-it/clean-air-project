import os
import subprocess
import sys

import streamlit as st

# -----------------------------------------------------
# 1. AUTO-INSTALL MISSING DEPENDENCIES
# -----------------------------------------------------
REQUIRED_PACKAGES = [
    "plotly",
    "pandas",
    "requests"
]

def ensure_dependencies(packages):
    """Automatically install missing dependencies at runtime."""
    missing = []
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)

    if missing:
        st.warning(f"Installing missing dependencies: {', '.join(missing)}")
        for pkg in missing:
            subprocess.run([sys.executable, "-m", "pip", "install", pkg])
        st.success("Dependencies installed! Please rerun the app.")
        st.stop()

ensure_dependencies(REQUIRED_PACKAGES)

# Safe imports AFTER ensuring packages exist
import pandas as pd
import plotly.express as px
import requests


# -----------------------------------------------------
# 2. PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="Clean Air Project – Demo Dashboard",
    layout="wide",
)


# -----------------------------------------------------
# 3. DEMO DATA GENERATION (until your backend API is ready)
# -----------------------------------------------------
def load_demo_data():
    """Creates a small data sample for testing the dashboard."""
    data = {
        "pm25": [8, 15, 22, 35, 18, 9],
        "pm10": [12, 20, 40, 65, 25, 10],
        "temperature": [21.5, 22.2, 22.0, 21.0, 20.5, 20.8],
        "humidity": [45, 47, 50, 55, 48, 46],
        "lat": [36.1627] * 6,      # Nashville placeholder
        "lon": [-86.7816] * 6,
        "timestamp": pd.date_range(end=pd.Timestamp.now(), periods=6)
    }
    return pd.DataFrame(data)


# -----------------------------------------------------
# 4. OPTIONAL: AUTO SEND DEMO PAYLOAD TO API
# -----------------------------------------------------
def send_demo_payload():
    """Send a simple example message to your API."""
    api_url = st.session_state.get("api_url", "").strip()
    if not api_url:
        st.error("No API URL configured.")
        return

    sample_payload = {
        "device_id": "demo-node",
        "pm25": 12,
        "pm10": 25,
        "humidity": 45,
        "temperature": 22.1
    }

    try:
        r = requests.post(api_url, json=sample_payload)
        st.info(f"API Response: {r.status_code} – {r.text}")
    except Exception as e:
        st.error(f"Failed to send demo payload: {e}")


# -----------------------------------------------------
# 5. UI LAYOUT
# -----------------------------------------------------
st.title("🌱 Clean Air Project – Data Dashboard")
st.write("This dashboard loads demo sensor data and displays visualizations.")


# API URL input (optional)
st.sidebar.header("API Demo Tools")
st.sidebar.text_input("API URL", key="api_url")
if st.sidebar.button("Send Demo Payload"):
    send_demo_payload()


# -----------------------------------------------------
# 6. LOAD + DISPLAY DATA
# -----------------------------------------------------
df = load_demo_data()

st.subheader("Raw Data Sample")
st.dataframe(df)


# -----------------------------------------------------
# 7. VISUALIZATIONS
# -----------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    fig_pm25 = px.line(
        df,
        x="timestamp",
        y="pm25",
        title="PM2.5 Levels Over Time",
    )
    st.plotly_chart(fig_pm25, use_container_width=True)

with col2:
    fig_pm10 = px.line(
        df,
        x="timestamp",
        y="pm10",
        title="PM10 Levels Over Time",
    )
    st.plotly_chart(fig_pm10, use_container_width=True)


# -----------------------------------------------------
# 8. MAP VIS
# -----------------------------------------------------
st.subheader("Sensor Map (Demo Coordinates)")

fig_map = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    hover_name="pm25",
    zoom=9,
    size_max=12,
)

fig_map.update_layout(mapbox_style="open-street-map")
st.plotly_chart(fig_map, use_container_width=True)

import os
import time
from datetime import datetime
from pathlib import Path
import json
import requests

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import markdown2

# ----------------------------
# CONFIG
# ----------------------------
st.set_page_config(page_title="Clean Air Control Center", layout="wide", page_icon="🫁")
ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT.joinpath("..", "docs")  # relative to dashboard/
API_DEFAULT = os.getenv("API_URL", "").rstrip("/")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or (st.secrets.get("GITHUB_TOKEN") if "GITHUB_TOKEN" in st.secrets else None)
GITHUB_REPO = os.getenv("GITHUB_REPO") or (st.secrets.get("GITHUB_REPO") if "GITHUB_REPO" in st.secrets else None)
GITHUB_WORKFLOW_ID = os.getenv("GITHUB_WORKFLOW_ID") or (st.secrets.get("GITHUB_WORKFLOW_ID") if "GITHUB_WORKFLOW_ID" in st.secrets else None)

# Demo API file hosted on GitHub Pages (if you used the earlier step)
PUBLIC_JSON = f"https://{GITHUB_REPO.replace('/', '.')}.github.io/{GITHUB_REPO.split('/')[-1]}/api/air.json" if GITHUB_REPO else None

# Fallback local demo data file (we created earlier)
DEMO_CSV = ROOT.joinpath("sensor_data.csv")
DEMO_JSON = ROOT.joinpath("demo_data.json")

# ----------------------------
# Helpers
# ----------------------------
@st.cache_data(ttl=60)
def load_api_data(api_url):
    """Load JSON array or object{data:[]} from an API url; returns DataFrame."""
    try:
        r = requests.get(api_url, timeout=6)
        r.raise_for_status()
        payload = r.json()
        if isinstance(payload, dict) and "data" in payload:
            df = pd.DataFrame(payload["data"])
        elif isinstance(payload, list):
            df = pd.DataFrame(payload)
        elif isinstance(payload, dict) and "device_id" in payload and "data" in payload:
            df = pd.DataFrame(payload["data"])
        else:
            # best-effort: try to convert dict->one row
            df = pd.DataFrame([payload]) if isinstance(payload, dict) else pd.DataFrame()
        # normalize timestamp
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        return df
    except Exception as e:
        return pd.DataFrame()

@st.cache_data(ttl=60)
def load_local_demo():
    """Load CSV or JSON fallback."""
    if DEMO_CSV.exists():
        try:
            df = pd.read_csv(DEMO_CSV)
            if "timestamp" in df.columns:
                df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            return df
        except Exception:
            pass
    # create small demo set inline
    now = datetime.utcnow()
    rows = []
    for i in range(12):
        rows.append({
            "timestamp": (now - pd.Timedelta(minutes=5*(12-i))).isoformat(),
            "pm25": float(np.random.randint(5, 80)),
            "temperature": float(18 + np.random.rand()*8),
            "humidity": float(35 + np.random.rand()*40),
            "lat": 37.7749 + np.random.uniform(-0.02, 0.02),
            "lon": -122.4194 + np.random.uniform(-0.02, 0.02),
            "device_id": "demo-01",
        })
    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

def compute_aqi_simple(pm25):
    # simplified EPA-like mapping for display
    try:
        pm25 = float(pm25)
    except Exception:
        return None
    if pm25 <= 12:
        return round(50 * pm25 / 12)
    if pm25 <= 35.4:
        return round(50 + (pm25-12)*(50/23.4))
    if pm25 <= 55.4:
        return round(100 + (pm25-35.4)*(50/20))
    return 200

def dispatch_github_workflow(repo, workflow_id, ref="main", inputs=None, token=None):
    """Dispatch a repository workflow (requires repo, workflow file name or id, token)."""
    if token is None:
        return False, "No token provided"
    url = f"https://api.github.com/repos/{repo}/actions/workflows/{workflow_id}/dispatches"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github+json"}
    body = {"ref": ref}
    if inputs:
        body["inputs"] = inputs
    r = requests.post(url, headers=headers, json=body, timeout=10)
    if r.status_code in (204, 201):
        return True, f"Workflow dispatched (HTTP {r.status_code})"
    return False, f"Failed ({r.status_code}): {r.text}"

def post_demo_to_api(api_url, payload):
    try:
        r = requests.post(api_url, json=payload, timeout=6)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

# ----------------------------
# Layout: sidebar controls
# ----------------------------
st.sidebar.title("Clean Air Control Center")
st.sidebar.markdown("Primary controls and quick links for project operations")

# Data source selection
data_source = st.sidebar.selectbox("Load data from:", ["Demo (local)", "Public JSON (gh-pages)", "Custom API URL"])
api_url_input = st.sidebar.text_input("Custom API URL", value=API_DEFAULT if API_DEFAULT else "")

# GitHub action dispatch
st.sidebar.markdown("---")
st.sidebar.subheader("Automation")
gh_dispatch = st.sidebar.checkbox("Enable workflow dispatch buttons", value=bool(GITHUB_TOKEN and GITHUB_REPO))
if gh_dispatch:
    st.sidebar.markdown(f"Repo: `{GITHUB_REPO}`")
    workflow_ref = st.sidebar.text_input("Workflow filename or id", value=GITHUB_WORKFLOW_ID if GITHUB_WORKFLOW_ID else "")
    workflow_branch = st.sidebar.text_input("Ref/branch to run", value="main")
else:
    workflow_ref = ""
    workflow_branch = "main"

st.sidebar.markdown("---")
st.sidebar.markdown("Quick links")
st.sidebar.markdown(f"- [GitHub Repo](https://github.com/{GITHUB_REPO})" if GITHUB_REPO else "- Add GITHUB_REPO to enable links")
st.sidebar.markdown("- [Docs site](/site/)")

# ----------------------------
# Main app: Tabs for different aspects
# ----------------------------
tabs = st.tabs(["Dashboard", "Map", "Docs & Training", "Schematics / Assets", "Firmware & CI", "Operations"])

# ----------------------------
# TAB: Dashboard (data summary + charts)
# ----------------------------
with tabs[0]:
    st.header("Live Data Dashboard")
    if data_source == "Demo (local)":
        df = load_local_demo()
        source_label = "Local Demo Data"
    elif data_source == "Public JSON (gh-pages)":
        if PUBLIC_JSON:
            df = load_api_data(PUBLIC_JSON)
            source_label = f"Public JSON ({PUBLIC_JSON})"
        else:
            st.warning("No public JSON mapped: set GITHUB_REPO env/secrets.")
            df = load_local_demo()
            source_label = "Fallback demo"
    else:
        # custom API
        if api_url_input.strip():
            df = load_api_data(api_url_input.strip())
            source_label = f"Custom API ({api_url_input})"
        else:
            st.warning("No API URL provided; falling back to demo data.")
            df = load_local_demo()
            source_label = "Fallback demo"

    st.caption(f"Data source: {source_label}")

    if df.empty:
        st.warning("No data available for selected source.")
    else:
        # normalize columns
        df = df.copy()
        df.columns = [c.lower() for c in df.columns]
        if "timestamp" in df.columns:
            df = df.sort_values("timestamp")
        else:
            df["timestamp"] = pd.to_datetime(datetime.utcnow())

        # compute AQI
        df["aqi"] = df["pm25"].apply(lambda v: compute_aqi_simple(v) if pd.notnull(v) else np.nan)

        # top metrics
        latest = df.iloc[-1]
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Latest PM2.5", f"{latest.get('pm25', 'n/a')}")
        col2.metric("Latest AQI (est.)", f"{int(latest.get('aqi', 0))}")
        col3.metric("Temp (°C)", f"{latest.get('temperature', 'n/a')}")
        col4.metric("Humidity (%)", f"{latest.get('humidity', 'n/a')}")

        st.markdown("### PM2.5 over time")
        if "timestamp" in df.columns and "pm25" in df.columns:
            fig = px.line(df, x="timestamp", y="pm25", title="PM2.5 (µg/m³)")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No timestamp/pm25 columns found")

        st.markdown("### Recent readings")
        st.dataframe(df.tail(100))

# ----------------------------
# TAB: Map
# ----------------------------
with tabs[1]:
    st.header("Sensor Map")
    # Use the same df chosen in Dashboard tab
    try:
        if df.empty:
            st.info("No data available to map.")
        elif {"lat", "lon"}.issubset(set(df.columns)):
            map_df = df.dropna(subset=["lat", "lon"])[["lat", "lon", "pm25", "device_id", "timestamp"]].copy()
            # ensure numeric
            map_df["lat"] = pd.to_numeric(map_df["lat"], errors="coerce")
            map_df["lon"] = pd.to_numeric(map_df["lon"], errors="coerce")
            if map_df.empty:
                st.info("No valid lat/lon values found.")
            else:
                st.map(map_df.rename(columns={"lat":"lat", "lon":"lon"})[["lat", "lon"]])
                st.markdown("**Points** (most recent per location):")
                st.dataframe(map_df.sort_values("timestamp").drop_duplicates(subset=["lat","lon"], keep="last").tail(50))
        else:
            st.info("Data does not include 'lat' and 'lon' fields. You can add them in the data source.")
    except Exception as e:
        st.error(f"Map error: {e}")

# ----------------------------
# TAB: Docs & Training
# ----------------------------
with tabs[2]:
    st.header("Documentation & Training Materials")
    st.markdown("Quick access to key docs and training content hosted in the repo's `docs/` folder.")

    docs_files = []
    docs_path = (ROOT / ".." / "docs").resolve()
    if docs_path.exists():
        for md in docs_path.rglob("*.md"):
            docs_files.append(md.relative_to(docs_path))
    docs_files = sorted(set(docs_files))
    if not docs_files:
        st.info("No docs found in docs/ — add your Markdown docs there.")
    else:
        sel = st.selectbox("Open doc", options=["-- choose --"] + [str(p) for p in docs_files])
        if sel and sel != "-- choose --":
            mdpath = docs_path.joinpath(sel)
            text = mdpath.read_text(encoding="utf-8")
            html = markdown2.markdown(text, extras=["fenced-code-blocks", "tables"])
            st.markdown(html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Training materials")
    # we can list PDFs or slides in docs/training or assets
    training_dir = docs_path.joinpath("training")
    if training_dir.exists():
        for f in training_dir.iterdir():
            if f.suffix.lower() in [".pdf", ".pptx", ".ppt"]:
                st.markdown(f"- [{f.name}]({str(f.relative_to(docs_path))})")
    else:
        st.info("No training/ folder found in docs/. You can add handouts, slides, and PDFs there.")

# ----------------------------
# TAB: Schematics / Assets
# ----------------------------
with tabs[3]:
    st.header("Schematics & Assets")
    assets_dir = (ROOT / ".." / "docs" / "assets").resolve()
    if assets_dir.exists():
        imgs = list(assets_dir.glob("*.*"))
        if not imgs:
            st.info("No assets found in docs/assets/")
        else:
            cols = st.columns(3)
            for i, img in enumerate(imgs):
                try:
                    with cols[i % 3]:
                        st.image(str(img), caption=img.name, use_column_width=True)
                except Exception:
                    st.text(f"Can't render {img.name}")
    else:
        st.info("No docs/assets folder found. Place your PNG/SVG schematics there.")

# ----------------------------
# TAB: Firmware & CI
# ----------------------------
with tabs[4]:
    st.header("Firmware & CI")
    st.markdown("This section surfaces the firmware folder, PlatformIO, and CI workflow files.")

    firmware_path = (ROOT / ".." / "firmware").resolve()
    if firmware_path.exists():
        st.markdown(f"Firmware folder: `{firmware_path}`")
        # list src files
        src = firmware_path.joinpath("src")
        if src.exists():
            files = list(src.rglob("*.*"))
            st.markdown("**Source files**")
            for f in sorted(files):
                st.write(f"- `{f.relative_to(firmware_path)}`")
        else:
            st.info("No firmware/src found yet.")
    else:
        st.info("No firmware/ folder found. Add your PlatformIO project there.")

    st.markdown("---")
    st.markdown("CI / Workflows in .github/workflows")
    gh = (ROOT / ".." / ".github" / "workflows").resolve()
    if gh.exists():
        for wf in gh.glob("*.yml"):
            st.write(f"- `{wf.name}`")
    else:
        st.info("No workflows found.")

# ----------------------------
# TAB: Operations (demo injector + GH dispatch)
# ----------------------------
with tabs[5]:
    st.header("Operations")

    st.markdown("### 1) Inject demo reading to API (POST)")
    st.markdown("Use this to push a single sample reading to your API endpoint. Useful for testing the dashboard or ingestion flow.")
    api_target = st.text_input("API endpoint to POST (example: https://example.com/api/data)", value=(api_url_input or API_DEFAULT or ""))
    col_a, col_b = st.columns(2)
    with col_a:
        demo_pm = st.number_input("pm2.5 value", value=42.0, step=0.1)
        demo_temp = st.number_input("temperature (°C)", value=22.5, step=0.1)
        demo_hum = st.number_input("humidity (%)", value=55.0, step=0.1)
    with col_b:
        demo_lat = st.number_input("lat", value=37.7749, format="%.6f")
        demo_lon = st.number_input("lon", value=-122.4194, format="%.6f")
        demo_dev = st.text_input("device_id", value="demo-injector")

    if st.button("Send demo reading now"):
        if not api_target:
            st.error("Provide an API endpoint before sending.")
        else:
            payload = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "pm25": float(demo_pm),
                "temperature": float(demo_temp),
                "humidity": float(demo_hum),
                "lat": float(demo_lat),
                "lon": float(demo_lon),
                "device_id": demo_dev
            }
            code, resp = post_demo_to_api(api_target, payload)
            if code is None:
                st.error(f"Request error: {resp}")
            else:
                st.success(f"POST {code}: {resp}")

    st.markdown("---")
    st.markdown("### 2) Dispatch GitHub workflow (if token set)")
    if not GITHUB_TOKEN:
        st.warning("No GITHUB_TOKEN available (set env or Streamlit secrets to enable).")
    else:
        st.markdown(f"Repo: `{GITHUB_REPO}`")
        wf_to_run = st.text_input("Workflow filename/id", value=workflow_ref or "")
        wf_ref = st.text_input("Ref/branch", value=workflow_branch or "main")
        btn = st.button("Dispatch workflow")
        if btn:
            if not (GITHUB_REPO and wf_to_run):
                st.error("Set GITHUB_REPO and workflow name.")
            else:
                ok, msg = dispatch_github_workflow(GITHUB_REPO, wf_to_run, ref=wf_ref, inputs=None, token=GITHUB_TOKEN)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

    st.markdown("---")
    st.markdown("### 3) Maintenance")
    st.markdown("- Download logs / CSV from the Dashboard tab and archive them.")
    if st.button("Export latest dataset to CSV"):
        if df.empty:
            st.info("No data to export.")
        else:
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "clean-air-latest.csv", "text/csv")

# ----------------------------
# Footer / help
# ----------------------------
st.markdown("---")
st.caption("Clean Air Project — unified control center. Keep tokens private; do not expose secrets in public repos.")
        
