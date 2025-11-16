import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
from datetime import datetime

st.set_page_config(page_title="Clean Air Dashboard", layout="wide")

API_URL = "https://YOUR_API_URL_HERE/api/data"   # replace with real API endpoint

# ---------------------------
# LOAD DATA FROM API
# ---------------------------
def load_data():
    try:
        r = requests.get(API_URL, timeout=5)
        if r.status_code == 200:
            data = r.json()
            return pd.DataFrame(data)
        else:
            st.error(f"API error: {r.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return pd.DataFrame()

# ---------------------------
# SIDEBAR
# ---------------------------
st.sidebar.header("Dashboard Controls")
demo_mode = st.sidebar.checkbox("Enable demo mode (generate fake data)", value=True)
refresh = st.sidebar.button("Refresh Now")

# ---------------------------
# DEMO MODE — LOCAL FAKE DATA
# ---------------------------
def generate_demo_data(n=20):
    np.random.seed(42)

    demo = {
        "timestamp": [datetime.utcnow().isoformat()] * n,
        "pm25": np.random.randint(5, 150, n),
        "temperature": np.random.uniform(15, 30, n),
        "humidity": np.random.uniform(30, 80, n),
        # Map requires lat/long — now provided!
        "lat": np.random.uniform(37.76, 37.80, n),
        "lon": np.random.uniform(-122.49, -122.39, n),
    }
    return pd.DataFrame(demo)

# Load real or demo data
if demo_mode:
    df = generate_demo_data()
else:
    df = load_data()

# ---------------------------
# MAIN UI
# ---------------------------
st.title("🌎 Clean Air Project Dashboard")

if df.empty:
    st.warning("No data available.")
    st.stop()

# ---------------------------
# METRICS CARDS
# ---------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Average PM2.5", f"{df['pm25'].mean():.1f} µg/m³")
col2.metric("Temperature", f"{df['temperature'].mean():.1f} °C")
col3.metric("Humidity", f"{df['humidity'].mean():.1f} %")

st.divider()

# ---------------------------
# CHARTS
# ---------------------------
st.subheader("PM2.5 Over Time")
st.line_chart(df[['pm25']])

st.subheader("Temperature Over Time")
st.line_chart(df[['temperature']])

st.subheader("Humidity Over Time")
st.line_chart(df[['humidity']])

st.divider()

# ---------------------------
# MAP VISUALIZATION 
# ---------------------------
st.subheader("Sensor Locations")

if "lat" not in df.columns or "lon" not in df.columns:
    st.error("Map requires 'lat' and 'lon' fields.")
else:
    st.map(df[['lat', 'lon']])

st.success("Dashboard loaded successfully!")

#----------------------------
# THREE-D HEATMAP
#----------------------------
!-- tools/cesium_starter.html -->
<!doctype html>
<html>
<head>
  <title>Clean Air ThreeD</title>
  <script src="https://cesium.com/downloads/cesiumjs/releases/1.115/Build/Cesium/Cesium.js"></script>
  <link href="https://cesium.com/downloads/cesiumjs/releases/1.115/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
</head>
<body>
  <div id="cesiumContainer" style="width:100%;height:100vh;"></div>
  <script>
    const viewer = new Cesium.Viewer('cesiumContainer', {terrainProvider: Cesium.createWorldTerrain()});
    // load your points from JSON (fetch('/api/air.json')) and create entities
  </script>
</body>
</html>
