# Green Tools — Clean Air Project

This folder contains scripts and data to:
- map tree placements (with or without lat/lon),
- estimate cost & maintenance,
- estimate stormwater benefits,
- approximate pollutant removal (PM2.5, O3, NO2, SO2),
- provide species icons,
- propose recommended trees using a simple AI-suggester,
- run multi-year CO2 & PM accumulation simulations.

**How to use**
1. Install dependencies:

pip install pandas folium matplotlib

For Streamlit integration also install:

pip install streamlit pydeck paho-mqtt

2. Run examples:

python map_trees.py python pollutant_model.py python simulation.py

**Data**
- `trees_catalog.csv` stores species parameters used in modeling.

**Notes**
- Models are heuristic; replace coefficients with local references for higher accuracy.
- 
