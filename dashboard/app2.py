# dashboard/app.py
import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import os
from datetime import datetime
import pydeck as pdk

# local mqtt helper (background thread + queue)
from mqtt_client import MQTTThread, mqtt_queue

st.set_page_config(page_title="Clean Air Dashboard", layout="wide", page_icon="🫁")

# -----------------------
# CONFIG / DEFAULTS
# -----------------------
DEFAULT_API_URL = "https://mamaofthree579-ship-it.github.io/clean-air-project/api/air.json"
DEFAULT_MQTT_BROKER = os.getenv("MQTT_BROKER", "")
DEFAULT_MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
DEFAULT_MQTT_TOPIC = os.getenv("MQTT_TOPIC", "clean_air/+/data")

# session init
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame()
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame()
if "mqtt_thread" not in st.session_state:
    st.session_state.mqtt_thread = None
if "mqtt_connected" not in st.session_state:
    st.session_state.mqtt_connected = False
if "last_update" not in st.session_state:
    st.session_state.last_update = None

# -----------------------
# SIDEBAR CONTROLS
# -----------------------
st.sidebar.title("Data Sources")
use_rest = st.sidebar.checkbox("Use REST API", value=True)
api_url = st.sidebar.text_input("REST API URL", value=DEFAULT_API_URL if use_rest else "")
use_mqtt = st.sidebar.checkbox("Use MQTT", value=False)

mqtt_broker = st.sidebar.text_input("MQTT Broker", value=DEFAULT_MQTT_BROKER)
mqtt_port = st.sidebar.number_input("MQTT Port", value=DEFAULT_MQTT_PORT, step=1)
mqtt_topic = st.sidebar.text_input("MQTT Topic (subscribe)", value=DEFAULT_MQTT_TOPIC)

st.sidebar.markdown("---")
st.sidebar.markdown("**Controls**")
if st.sidebar.button("Force refresh"):
    # clearing cache by toggling a key
    st.session_state.last_update = None

# -----------------------
# REST loader
# -----------------------
def load_rest(api_url):
    try:
        resp = requests.get(api_url, timeout=6)
        resp.raise_for_status()
        j = resp.json()
        # Depending on format: our GitHub JSON had a "data" array
        if isinstance(j, dict) and "data" in j:
            df = pd.DataFrame(j["data"])
        else:
            # maybe array at top
            df = pd.DataFrame(j)
        # Try to normalize timestamp
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])
        else:
            # add now timestamps if missing
            df["timestamp"] = pd.to_datetime(datetime.utcnow())
        return df
    except Exception as e:
        st.sidebar.error(f"REST load error: {e}")
        return pd.DataFrame()

# -----------------------
# MQTT start/stop
# -----------------------
def ensure_mqtt_thread(broker, port, topic):
    # Start the background MQTT thread if not running
    if st.session_state.mqtt_thread is None or not st.session_state.mqtt_thread.is_alive():
        try:
            th = MQTTThread(broker, port, topic)
            th.start()
            st.session_state.mqtt_thread = th
            st.session_state.mqtt_connected = True
            st.sidebar.success("MQTT thread started")
        except Exception as e:
            st.sidebar.error(f"MQTT start failed: {e}")
            st.session_state.mqtt_connected = False

def stop_mqtt_thread():
    try:
        if st.session_state.mqtt_thread:
            st.session_state.mqtt_thread.stop()
            st.session_state.mqtt_thread = None
            st.session_state.mqtt_connected = False
            st.sidebar.warning("MQTT stopped")
    except Exception as e:
        st.sidebar.error(f"Error stopping MQTT: {e}")

# start or stop mqtt based on toggle
if use_mqtt:
    if not mqtt_broker:
        st.sidebar.warning("Provide MQTT broker to enable MQTT")
    else:
        ensure_mqtt_thread(mqtt_broker, mqtt_port, mqtt_topic)
else:
    # stop thread if running
    if st.session_state.mqtt_thread:
        stop_mqtt_thread()

# -----------------------
# Data ingestion loop
# -----------------------
def ingest_mqtt_queue():
    updated = False
    while not mqtt_queue.empty():
        obj = mqtt_queue.get_nowait()
        # meta messages
        if "__meta__" in obj:
            # show simple messages in sidebar
            st.sidebar.info(f"MQTT: {obj['__meta__']}")
            continue

        # Try to normalize to DataFrame row(s)
        if isinstance(obj, dict):
            row = obj.copy()
            # some payloads may contain 'timestamp' or 'time'
            if "timestamp" in row:
                try:
                    row["timestamp"] = pd.to_datetime(row["timestamp"])
                except:
                    row["timestamp"] = pd.to_datetime(datetime.utcnow())
            else:
                row["timestamp"] = pd.to_datetime(datetime.utcnow())
            # push into session data
            df_row = pd.DataFrame([row])
            if st.session_state.data.empty:
                st.session_state.data = df_row
            else:
                st.session_state.data = pd.concat([st.session_state.data, df_row], ignore_index=True)
            updated = True
    return updated

def ingest_rest_data(df):
    if df.empty:
        return False
    # append new rows if any
    if st.session_state.data.empty:
        st.session_state.data = df
        return True
    else:
        st.session_state.data = pd.concat([st.session_state.data, df], ignore_index=True)
        return True

# -----------------------
# Pull REST now if enabled
# -----------------------
if use_rest and api_url:
    df_rest = load_rest(api_url)
    if not df_rest.empty:
        ingest_rest_data(df_rest)

# Pull MQTT queue messages
if use_mqtt and st.session_state.mqtt_thread:
    try:
        updated = ingest_mqtt_queue()
    except Exception as e:
        st.sidebar.error(f"MQTT ingest error: {e}")

# basic cleanup: keep last N rows
if not st.session_state.data.empty:
    # normalize column names
    st.session_state.data.columns = [c.lower() for c in st.session_state.data.columns]
    # ensure timestamp
    if "timestamp" not in st.session_state.data.columns:
        st.session_state.data["timestamp"] = pd.to_datetime(datetime.utcnow())
    else:
        st.session_state.data["timestamp"] = pd.to_datetime(st.session_state.data["timestamp"], errors="coerce")
    st.session_state.data = st.session_state.data.sort_values("timestamp").drop_duplicates().reset_index(drop=True)
    # keep last 1000 rows
    if len(st.session_state.data) > 2000:
        st.session_state.data = st.session_state.data.iloc[-2000:].reset_index(drop=True)
    st.session_state.last_update = datetime.utcnow().isoformat()

# -----------------------
# UI: Header / metrics
# -----------------------
st.title("🫁 Clean Air Project — Live Dashboard")
if st.session_state.last_update:
    st.caption(f"Last update: {st.session_state.last_update}")

if st.session_state.data.empty:
    st.warning("No data ingested yet. Use REST or MQTT to populate.")
    st.stop()

# extract latest reading
latest = st.session_state.data.iloc[-1]

col1, col2, col3, col4 = st.columns(4)
pm25_value = latest.get("pm25") or latest.get("pm2_5") or latest.get("pm2.5") or np.nan
col1.metric("PM2.5 (µg/m³)", f"{pm25_value:.1f}" if not np.isnan(pm25_value) else "n/a")
col2.metric("Temp (°C)", f"{latest.get('temperature', 'n/a')}")
col3.metric("Humidity (%)", f"{latest.get('humidity', 'n/a')}")
col4.metric("Devices (rows)", len(st.session_state.data))

# -----------------------
# Time series plot
# -----------------------
st.subheader("PM2.5 Over Time")
if "timestamp" in st.session_state.data.columns and not st.session_state.data["timestamp"].isnull().all():
    ts_df = st.session_state.data[["timestamp"]].copy()
    # try to extract numeric PM2.5 columns
    if "pm25" in st.session_state.data.columns:
        ts_df["pm25"] = st.session_state.data["pm25"].astype(float)
    elif "pm2_5" in st.session_state.data.columns:
        ts_df["pm25"] = st.session_state.data["pm2_5"].astype(float)
    elif "pm2.5" in st.session_state.data.columns:
        ts_df["pm25"] = st.session_state.data["pm2.5"].astype(float)
    else:
        ts_df["pm25"] = np.nan

    ts_df = ts_df.dropna(subset=["pm25"])
    if not ts_df.empty:
        st.line_chart(ts_df.rename(columns={"timestamp":"index"}).set_index("index")["pm25"])
    else:
        st.info("No PM2.5 numeric column found for chart.")
else:
    st.info("No timestamp column available for timeseries.")

# -----------------------
# Live Map (pydeck)
# -----------------------
st.subheader("Sensor Map")
if {"lat", "lon"}.issubset(set(st.session_state.data.columns)):
    map_df = st.session_state.data.dropna(subset=["lat","lon"])[["lat","lon","pm25","timestamp"]].copy()
    # keep most recent per location (by lat/lon)
    map_df = map_df.sort_values("timestamp").drop_duplicates(subset=["lat","lon"], keep="last")
    if not map_df.empty:
        midpoint = (map_df["lat"].mean(), map_df["lon"].mean())
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position=["lon", "lat"],
            get_fill_color=["pm25", 100 - map_df["pm25"], 50],
            get_radius=200,
            pickable=True
        )
        view_state = pdk.ViewState(latitude=midpoint[0], longitude=midpoint[1], zoom=10)
        r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text":"PM2.5: {pm25}\nTime: {timestamp}"})
        st.pydeck_chart(r, use_container_width=True)
    else:
        st.info("No geolocated records found to display.")
else:
    st.info("No lat/lon columns present. Provide 'lat' and 'lon' fields to show sensors on map.")

# -----------------------
# Device Table & raw data
# -----------------------
st.subheader("Recent Records")
st.dataframe(st.session_state.data.tail(200))

# -----------------------
# Shutdown hazard: stop mqtt thread when session ends (manual button)
# -----------------------
if st.button("Stop MQTT (if running)"):
    stop_mqtt_thread()
    st.sidebar.success("Stopped MQTT thread.")

