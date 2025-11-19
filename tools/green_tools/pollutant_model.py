# tools/green_tools/pollutant_model.py
import pandas as pd
import math
from pathlib import Path
CATALOG = Path(__file__).parent / "trees_catalog.csv"

def per_tree_yearly_removal(species_key):
    """
    Returns dict of yearly removal masses for PM2.5 (g), O3 (g), NO2 (g), SO2 (g), and CO2 (kg)
    based on catalog. These are estimates suitable for planning.
    """
    df = pd.read_csv(CATALOG)
    row = df[df['species'] == species_key].iloc[0]
    canopy_area_m2 = math.pi * (row['canopy_diameter_m']/2)**2
    pm_g = row['pm2_5_removal_g_m2_yr'] * canopy_area_m2
    co2_kg = row['co2_uptake_kg_tree_yr']
    return {
        "pm2_5_g_yr": pm_g,
        "co2_kg_yr": co2_kg,
        "o3_g_yr": row.get("ozone_removal_g_tree_yr", 0.5),
        "no2_g_yr": row.get("no2_removal_g_tree_yr", 0.3),
        "so2_g_yr": row.get("so2_removal_g_tree_yr", 0.2)
    }

def fleet_removal(species_key, count, years=10, degradation_rate=0.01):
    """
    Simulates multi-year removal from a fleet of identical trees, accounting for
    maturation (increase first few years) and small degradation (disease, mortality).
    """
    base = per_tree_yearly_removal(species_key)
    # maturation curve: ramp up to 100% over 5 years (linear)
    results = []
    for year in range(1, years+1):
        maturation_factor = min(1.0, year / 5.0)
        survival = (1 - degradation_rate) ** (year - 1)
        pm_total_g = base['pm2_5_g_yr'] * count * maturation_factor * survival
        co2_total_kg = base['co2_kg_yr'] * count * maturation_factor * survival
        o3 = base['o3_g_yr'] * count * maturation_factor * survival
        no2 = base['no2_g_yr'] * count * maturation_factor * survival
        so2 = base['so2_g_yr'] * count * maturation_factor * survival
        results.append({
            "year": year,
            "pm2_5_g": pm_total_g,
            "co2_kg": co2_total_kg,
            "o3_g": o3,
            "no2_g": no2,
            "so2_g": so2
        })
    return pd.DataFrame(results)

if __name__ == "__main__":
    print(fleet_removal("quercus_robur", 10, years=20).head())
  
