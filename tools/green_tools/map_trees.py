# tools/green_tools/map_trees.py
import folium
import pandas as pd
import math
from folium.features import DivIcon
from pathlib import Path

CATALOG = Path(__file__).parent / "trees_catalog.csv"
ICONS_DIR = Path(__file__).parent / "icons"

def bbox_to_grid(lat_min, lat_max, lon_min, lon_max, rows, cols):
    """Return list of (lat,lon) points grid inside bbox."""
    lats = [lat_min + (lat_max - lat_min) * (r + 0.5) / rows for r in range(rows)]
    lons = [lon_min + (lon_max - lon_min) * (c + 0.5) / cols for c in range(cols)]
    points = []
    for r in range(rows):
        for c in range(cols):
            points.append((lats[r], lons[c]))
    return points

def load_catalog():
    return pd.read_csv(CATALOG)

def default_map(center=(37.7749, -122.4194), zoom=12):
    m = folium.Map(location=center, zoom_start=zoom, tiles="CartoDB positron")
    return m

def add_tree_marker(m, lat, lon, species, common_name, canopy_m, icon_name=None):
    radius = max(5, min(30, canopy_m * 2))  # marker radius
    color = "#2b8cbe"
    folium.CircleMarker(
        location=(lat, lon),
        radius=radius,
        color=color,
        fill=True,
        fill_opacity=0.6,
        popup=f"{common_name} ({species}) — canopy ~{canopy_m} m"
    ).add_to(m)
    # Add small label
    folium.map.Marker(
        [lat, lon],
        icon=DivIcon(
            icon_size=(150,36),
            icon_anchor=(0,0),
            html=f'<div style="font-size:10px;color:#222">{common_name}</div>',
        )
    ).add_to(m)

def place_trees_from_catalog(m, bbox=None, grid=(3,4)):
    """
    Place sample trees using catalog.
    If bbox is provided (lat_min, lat_max, lon_min, lon_max) we will generate a grid.
    """
    df = load_catalog()
    if bbox:
        lat_min, lat_max, lon_min, lon_max = bbox
        pts = bbox_to_grid(lat_min, lat_max, lon_min, lon_max, rows=grid[0], cols=grid[1])
    else:
        # fallback: place around center
        center = m.location
        lat0, lon0 = center
        pts = [(lat0 + (i//4)*0.001, lon0 + (i%4)*0.001) for i in range(len(df))]
    for (lat, lon), (_, row) in zip(pts, df.iterrows()):
        add_tree_marker(m, lat, lon, row['species'], row['common_name'], row['canopy_diameter_m'], icon_name=row.get('icon'))

def save_map(m, path="tree_map.html"):
    m.save(path)
    print(f"Map saved to {path}")

if __name__ == "__main__":
    m = default_map()
    # Example bbox (SF area) or None
    bbox = (37.76, 37.79, -122.43, -122.39)
    place_trees_from_catalog(m, bbox=bbox, grid=(3,3))
    save_map(m)
  
