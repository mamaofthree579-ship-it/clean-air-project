import streamlit as st
import pandas as pd
import json
import random
import time
from pathlib import Path

st.set_page_config(
    page_title="Clean Air Project Dashboard",
    layout="wide"
)

DATA_FILE = Path("demo_data.json")


# ---------------------------
#  Create Local Demo Data File
# ---------------------------
def initialize_demo_data():
    """Create demo dataset if missing."""
    if not DATA_FILE.exists():
        demo = {
            "pm1_0": 3,
            "pm2_5": 5,
            "pm10": 8,
            "temperature": 22.1,
            "humidity": 41.5,
            "devices_online": 1
        }
        with open(DATA_FILE, "w") as f:
            json.dump(demo, f)


# ---------------------------
#  Load Demo Data
# ---------------------------
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


# ---------------------------
#  Simulate Updating Values
# ---------------------------
def simulate_update():
    data = load_data()

    def fluctuate(value, min_val, max_val):
        return max(min_val, min(max_val, value + random.uniform(-1, 1)))

    data["pm1_0"] = fluctuate(data["pm1_0"], 0, 50)
    data["pm2_5"] = fluctuate(data["pm2_5"], 0, 100)
    data["pm10"] = fluctuate(data["pm10"], 0, 150)
    data["temperature"] = fluctuate(data["temperature"], 15, 35)
    data["humidity"] = fluctuate(data["humidity"], 20, 80)
    data["devices_online"] = 1  # static for demo

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

    return data


# ---------------------------
#  UI Layout
# ---------------------------
st.title("🌍 Clean Air Project — Demo Dashboard")
st.subheader("Offline Version (Simulated Sensor Data)")


# Initialize data if missing
initialize_demo_data()

# Auto-update toggle
refresh = st.checkbox("Simulate Live Updates", value=True)

if refresh:
    data = simulate_update()
else:
    data = load_data()


# ---------------------------
#  Display Metric Cards
# ---------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("PM1.0 (µg/m³)", round(data["pm1_0"], 1))
col2.metric("PM2.5 (µg/m³)", round(data["pm2_5"], 1))
col3.metric("PM10 (µg/m³)", round(data["pm10"], 1))
col4.metric("Temperature (°C)", round(data["temperature"], 1))
col5.metric("Humidity (%)", round(data["humidity"], 1))

st.divider()

# ---------------------------
#  Graph (Historical Simulation)
# ---------------------------
st.subheader("Simulated Real-Time Chart")

# Add fake history
if "history" not in st.session_state:
    st.session_state.history = []

st.session_state.history.append([
    data["pm1_0"],
    data["pm2_5"],
    data["pm10"]
])

df = pd.DataFrame(st.session_state.history, columns=["PM1.0", "PM2.5", "PM10"])

st.line_chart(df)

# Auto-refresh every 2 seconds
if refresh:
    time.sleep(2)
    st.experimental_rerun()
