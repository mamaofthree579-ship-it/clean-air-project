#!/usr/bin/env python3
# tools/heatmap.py
import requests, pandas as pd, folium, os
from folium.plugins import HeatMap

# CONFIG
API_JSON = "https://mamaofthree579-ship-it.github.io/clean-air-project/api/air.json"
LOCAL_CSV = "dashboard/sensor_data.csv"   # fallback
OUT_HTML = "site/heatmap.html"

def load_df():
    try:
        r = requests.get(API_JSON, timeout=6)
        r.raise_for_status()
        j = r.json()
        if isinstance(j, dict) and "data" in j:
            df = pd.DataFrame(j["data"])
        else:
            df = pd.DataFrame(j)
    except Exception:
        df = pd.read_csv(LOCAL_CSV)
    # normalize columns
    df = df.rename(columns={c:c.lower() for c in df.columns})
    df = df.dropna(subset=["lat","lon","pm25"])
    df["pm25"] = pd.to_numeric(df["pm25"], errors="coerce").fillna(0)
    return df

def build_heatmap(df):
    if df.empty:
        raise RuntimeError("No data")
    # center map
    mid_lat, mid_lon = df["lat"].mean(), df["lon"].mean()
    m = folium.Map(location=[mid_lat, mid_lon], zoom_start=12, tiles="CartoDB positron")
    # prepare points as [lat, lon, weight]
    pts = df[["lat","lon","pm25"]].values.tolist()
    HeatMap(pts, radius=15, blur=12, max_zoom=13).add_to(m)
    # add popup points (optional)
    for _, r in df.iterrows():
        folium.CircleMarker([r.lat, r.lon],
                            radius=4,
                            color=None,
                            fill=True,
                            fill_opacity=0.7,
                            popup=f"pm2.5: {r.pm25}").add_to(m)
    os.makedirs(os.path.dirname(OUT_HTML) or ".", exist_ok=True)
    m.save(OUT_HTML)
    print("Saved heatmap:", OUT_HTML)

if __name__ == "__main__":
    df = load_df()
    build_heatmap(df)
