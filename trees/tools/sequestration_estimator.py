"""
Sequestration estimator (very simple model)
- Estimates annual carbon sequestration by species/DBH
- Uses rough lookup rates (tons CO2/year)
This is for ballpark estimates for reporting only.
"""

import csv
from datetime import datetime

# rough sequestration rates (kg CO2 per year) by tree size/class
# these numbers are illustrative — source local forestry tables for accuracy
SEQUESTRATION_RATES = {
    "small": 5.0,   # small tree ~5 kg CO2/yr
    "medium": 21.0, # medium ~21 kg CO2/yr
    "large": 48.0   # large ~48 kg CO2/yr
}

def estimate_from_registry(csv_path):
    total_kg = 0.0
    count = 0
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        for r in reader:
            count += 1
            # naive classifier by species or use 'notes'
            # for demo we assume medium
            total_kg += SEQUESTRATION_RATES['medium']
    return total_kg, count

if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "trees/data_templates/tree_registry.csv"
    kg, n = estimate_from_registry(path)
    print(f"{n} trees estimated to sequester ~{kg:.1f} kg CO2 per year (~{kg/1000:.2f} tCO2/yr).")
  
