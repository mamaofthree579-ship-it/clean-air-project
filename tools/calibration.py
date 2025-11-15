"""
Automatic sensor calibration tool.
Supports initial calibration and drift compensation using logged data.
"""

import numpy as np
import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def calibrate_offset(df):
    baseline = df["pm2_5_raw"].median()
    offset = 12.0 - baseline
    return offset

def save_calibration(offset, path="calibration.json"):
    import json
    with open(path, "w") as f:
        json.dump({"offset": offset}, f, indent=4)

if __name__ == "__main__":
    log = input("Path to sensor log CSV: ")
    df = load_data(log)

    offset = calibrate_offset(df)
    save_calibration(offset)

    print(f"Calibration offset generated: {offset}")
    print("Saved to calibration.json")
  
