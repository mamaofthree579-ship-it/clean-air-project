# tools/green_tools/cost_calculator.py
import pandas as pd
from pathlib import Path
CATALOG = Path(__file__).parent / "trees_catalog.csv"

def load_catalog():
    return pd.read_csv(CATALOG)

def cost_breakdown(species_key, quantity=1, years=10, discount_rate=0.03):
    df = load_catalog()
    row = df[df['species'] == species_key].iloc[0]
    plant_cost = row['establish_cost_usd'] * quantity
    annual_maint = row['annual_maintenance_usd'] * quantity
    # Present value of maintenance
    pv_maint = sum([annual_maint / ((1 + discount_rate) ** t) for t in range(1, years+1)])
    total_cost = plant_cost + pv_maint
    return {
        "species": row['common_name'],
        "quantity": quantity,
        "plant_cost": plant_cost,
        "pv_maintenance": round(pv_maint,2),
        "total_cost_{}_yr".format(years): round(total_cost,2)
    }

def cost_savings_estimate(species_key, quantity=1, years=10, avoided_health_cost_per_ugm3_per_person=0.02, population_served=100):
    """
    Heuristic: estimate annual health cost savings proportional to PM2.5 avoided.
    - avoided_health_cost_per_ugm3_per_person: $ per (µg/m³) per person per year
    - population_served: number of people benefiting from the planting (buffer)
    """
    df = load_catalog()
    row = df[df['species'] == species_key].iloc[0]
    canopy_area_m2 = math.pi * (row['canopy_diameter_m']/2)**2
    pm_removed_g_m2_yr = row['pm2_5_removal_g_m2_yr']
    # grams removed per tree per year:
    grams_removed = pm_removed_g_m2_yr * canopy_area_m2
    ug_removed = grams_removed * 1000  # convert g -> mg? careful: 1 g = 1e6 µg; correction:
    # Actually grams -> µg: *1e6
    ug_removed = grams_removed * 1e6
    # approximate µg/m³ reduction depends on buffer volume — we use a heuristic factor
    µg_m3_reduction_per_person = (ug_removed / 1e6) / 1000  # simplistic placeholder
    # monetary savings per year
    annual_savings = avoided_health_cost_per_ugm3_per_person * µg_m3_reduction_per_person * population_served
    return {"annual_savings_usd": round(annual_savings * quantity, 2), "ug_removed_per_tree_per_year": round(ug_removed,2)}

if __name__ == "__main__":
    import math
    print(cost_breakdown("quercus_robur", quantity=5))
    print(cost_savings_estimate("quercus_robur", quantity=5))
  
