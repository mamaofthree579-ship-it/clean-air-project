# tools/green_tools/stormwater.py
"""
Simple stormwater benefits estimator based on canopy interception and increased infiltration.

Based on:
- canopy interception percentage (fraction of rainfall intercepted by canopy and evaporated)
- increased infiltration per tree (m3 per event)
- peak flow reduction estimate

This is a simplified model for community planning, not hydrologic design.
"""

import math
from pathlib import Path
import pandas as pd
CATALOG = Path(__file__).parent / "trees_catalog.csv"

def tree_interception_volume(tree_canopy_m, rainfall_mm):
    """Estimate interception volume (m3) by canopy area and interception factor.
    rainfall_mm: mm of rainfall"""
    canopy_area_m2 = math.pi * (tree_canopy_m / 2)**2
    # interception fraction depends on species; assume 20-40%
    interception_fraction = 0.30
    # convert mm over m2 -> liters: mm * area -> liters (1 mm over 1 m2 = 1 L)
    liters = rainfall_mm * canopy_area_m2 * interception_fraction
    m3 = liters / 1000.0
    return m3

def infiltration_gain_per_tree(tree_canopy_m):
    """Estimate increased infiltration capacity per tree (m3 per year)"""
    # heuristics: small trees 0.5 m3/yr, medium 2 m3/yr, large 5 m3/yr
    if tree_canopy_m < 5:
        return 0.5
    elif tree_canopy_m < 10:
        return 2.0
    else:
        return 5.0

def stormwater_benefits(species_key, quantity=1, rainfall_mm=25):
    df = pd.read_csv(CATALOG)
    row = df[df['species'] == species_key].iloc[0]
    v_intercept = tree_interception_volume(row['canopy_diameter_m'], rainfall_mm) * quantity
    v_infil = infiltration_gain_per_tree(row['canopy_diameter_m']) * quantity
    return {
        "interception_m3_event": round(v_intercept,3),
        "annual_infiltration_m3": round(v_infil,3)
    }

if __name__ == "__main__":
    print(stormwater_benefits("quercus_robur", quantity=10, rainfall_mm=30))
  
