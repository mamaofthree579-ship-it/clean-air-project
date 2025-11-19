# tools/green_tools/tree_suggester.py
import pandas as pd
import math
from pathlib import Path
CATALOG = Path(__file__).parent / "trees_catalog.csv"

def score_tree(row, constraints):
    """
    constraints: dict with keys:
      - space_m2: available area per tree (m2)
      - pollution_priority: "pm" or "co2" or "stormwater" or "biodiversity"
      - drought_tolerance: boolean prefer
      - max_mature_height_m
    """
    score = 0.0
    # prioritize canopy size for PM capture
    if constraints.get("pollution_priority") == "pm":
        score += row['canopy_diameter_m'] * 2
    if constraints.get("pollution_priority") == "co2":
        score += row['co2_uptake_kg_tree_yr'] * 3
    if constraints.get("pollution_priority") == "stormwater":
        score += math.pi * (row['canopy_diameter_m']/2)**2 * 0.5
    # area constraint
    space = constraints.get("space_m2", 25)
    canopy_area = math.pi * (row['canopy_diameter_m']/2)**2
    if canopy_area > space:
        score -= 50  # too big
    # drought tolerance preference (if provided in catalog, not in sample)
    if constraints.get("drought_tolerance") and row.get("drought_tolerance", False):
        score += 5
    # avoid japanese maple for city street narrow planting
    if row['common_name'].lower().find("maple") != -1 and constraints.get("urban_street", False):
        score -= 8
    # cost sensitivity (prefer cheaper)
    score += max(0, 100 - row['establish_cost_usd'] / 5)
    return score

def suggest_trees(constraints, top_n=3):
    df = pd.read_csv(CATALOG)
    df['score'] = df.apply(lambda r: score_tree(r, constraints), axis=1)
    df_sorted = df.sort_values('score', ascending=False)
    return df_sorted.head(top_n)[['species','common_name','score','icon']]

if __name__ == "__main__":
    c = {"space_m2": 50, "pollution_priority":"pm", "urban_street":True}
    print(suggest_trees(c))
  
