import streamlit as st
import pandas as pd
import numpy as np
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# -------------------------------------------------------------------
# Page configuration
# -------------------------------------------------------------------
st.set_page_config(
    page_title="Community Air Quality Monitor",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 Community Air Quality Monitor Dashboard (Plotly-Free Version)")

st.markdown("""
This dashboard shows a live demonstration of air quality data (PM1.0 / PM2.5 / PM10)  
from sample sensor payloads. When your real sensors begin reporting, the graphs  
and map will update automatically.
""")

# -------------------------------------------------------------------
# SAMPLE DATA GENERATION
# -------------------------------------------------------------------
def generate_sample_data():
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=24, freq="H")
    return pd.DataFrame({
        "timestamp": timestamps,
        "pm1": np.random.randint(2, 20, len(timestamps)),
        "pm25": np.random.randint(5, 40, len(timestamps)),
        "pm10": np.random.randint(10, 60, len(timestamps)),
        "lat": 36.1627,   # Nashville default (replace later)
        "lon": -86.7816
    })

df = generate_sample_data()


# -------------------------------------------------------------------
# LAYOUT
# -------------------------------------------------------------------
col1, col2 = st.columns([1, 1])

# -------------------------------------------------------------------
# LEFT: Air Quality Charts (Matplotlib)
# -------------------------------------------------------------------
with col1:
    st.subheader("📈 Air Quality Levels (Past 24 Hours) — Matplotlib")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(df["timestamp"], df["pm1"], label="PM1.0")
    ax.plot(df["timestamp"], df["pm25"], label="PM2.5")
    ax.plot(df["timestamp"], df["pm10"], label="PM10")
    ax.set_xlabel("Time")
    ax.set_ylabel("µg/m³")
    ax.set_title("Particulate Matter Levels")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# -------------------------------------------------------------------
# RIGHT: Sensor Location Map (Folium)
# -------------------------------------------------------------------
with col2:
    st.subheader("🗺 Sensor Location Map")

    lat = df["lat"].iloc[-1]
    lon = df["lon"].iloc[-1]

    m = folium.Map(location=[lat, lon], zoom_start=10)

    folium.Marker(
        location=[lat, lon],
        popup="Sample Sensor Reading",
        tooltip="Sensor Node"
    ).add_to(m)

    st_map = st_folium(m, height=350, width="100%")


# -------------------------------------------------------------------
# LIVE PAYLOAD SIMULATION
# -------------------------------------------------------------------
st.subheader("📡 Incoming Payload Simulator")

if st.button("Push Sample Payload"):
    st.success("Sample payload sent (simulated). This will be replaced by live API ingestion.")

    st.json({
        "pm1": int(df["pm1"].iloc[-1]),
        "pm25": int(df["pm25"].iloc[-1]),
        "pm10": int(df["pm10"].iloc[-1]),
        "lat": lat,
        "lon": lon
    })


# -------------------------------------------------------------------
# RAW DATA VIEW
# -------------------------------------------------------------------
with st.expander("📄 Raw Data Table"):
    st.dataframe(df)
    
