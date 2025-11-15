import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from datetime import datetime, timedelta

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Clean Air Project Dashboard",
    page_icon="🫁",
    layout="wide"
)

API_URL = "https://example.com/api/air"   # Replace with real endpoint
LOCAL_FALLBACK = "sensor_data.csv"        # Will be used if API offline


# ---------------------------------------------------------
# LOAD DATA FUNCTION
# ---------------------------------------------------------
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_air_data():
    try:
        resp = requests.get(API_URL, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        df = pd.DataFrame(data)
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        return df, "Live API"
    except:
        # Fallback: local data file
        try:
            df = pd.read_csv(LOCAL_FALLBACK)
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            return df, "Local CSV"
        except:
            return None, "No Data Available"


# ---------------------------------------------------------
# AQI CALCULATION (Basic PM2.5 EPA formula)
# ---------------------------------------------------------
def calculate_aqi(pm25):
    if pm25 <= 12:
        return 50 * pm25 / 12
    elif pm25 <= 35.4:
        return 50 + (pm25 - 12) * (50 / 23.4)
    elif pm25 <= 55.4:
        return 100 + (pm25 - 35.4) * (50 / 20)
    else:
        return 200  # simplified for upper range


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("🫁 Clean Air Project")
st.sidebar.markdown("Community Air Quality Dashboard\n— *Live or Cached Data*")

refresh = st.sidebar.button("🔄 Refresh Data")


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
df, source = load_air_data()

if df is None:
    st.error("No sensor data available. Add a CSV or connect an API endpoint.")
    st.stop()

df["AQI"] = df["pm25"].apply(calculate_aqi)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("🫁 Clean Air Project — Community Air Quality Dashboard")
st.caption(f"Data Source: **{source}** — Last Updated: {datetime.now():%Y-%m-%d %H:%M:%S}")


# ---------------------------------------------------------
# TOP METRICS
# ---------------------------------------------------------
latest = df.sort_values("timestamp").iloc[-1]

col1, col2, col3 = st.columns(3)

col1.metric("PM2.5 (µg/m³)", f"{latest.pm25:.1f}")
col2.metric("Temperature (°C)", f"{latest.temperature:.1f}")
col3.metric("AQI", f"{latest.AQI:.0f}")


# ---------------------------------------------------------
# AQI Gauge Chart
# ---------------------------------------------------------
fig_gauge = px.scatter(
    x=[0], y=[latest.AQI],
    range_y=[0, 200],
    title="AQI Gauge",
)
fig_gauge.update_layout(height=200, showlegend=False)
st.plotly_chart(fig_gauge, use_container_width=True)


# ---------------------------------------------------------
# TIME SERIES
# ---------------------------------------------------------
st.subheader("📈 Air Quality Over Time")

fig_ts = px.line(
    df,
    x="timestamp",
    y="pm25",
    markers=True,
    title="PM2.5 Levels Over Time",
)
st.plotly_chart(fig_ts, use_container_width=True)


# ---------------------------------------------------------
# MAP (If GPS data exists)
# ---------------------------------------------------------
if "lat" in df.columns and "lon" in df.columns:
    st.subheader("🗺️ Sensor Map")
    st.map(df[["lat", "lon"]])
else:
    st.info("No GPS coordinates found; skipping map.")


# ---------------------------------------------------------
# DEVICE STATUS TABLE
# ---------------------------------------------------------
st.subheader("📟 Device Status")

device_cols = [c for c in df.columns if c not in ["pm25", "temperature", "timestamp", "AQI"]]

if device_cols:
    st.dataframe(df[["timestamp", "pm25", "temperature"] + device_cols].tail(20))
else:
    st.dataframe(df.tail(20))


# ---------------------------------------------------------
# RAW DATA DOWNLOAD
# ---------------------------------------------------------
st.subheader("⬇ Download Data")
st.download_button(
    label="Download CSV",
    data=df.to_csv(index=False),
    file_name="air_quality_data.csv",
    mime="text/csv",
)
