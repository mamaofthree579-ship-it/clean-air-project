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
