"""
Utility for analyzing long-term sensor logs and generating summaries.
"""

import pandas as pd

def analyze(path):
    df = pd.read_csv(path)
    summary = {
        "avg_pm25": df["pm2_5"].mean(),
        "max_pm25": df["pm2_5"].max(),
        "min_pm25": df["pm2_5"].min(),
        "avg_temp": df["temperature"].mean(),
        "avg_humidity": df["humidity"].mean()
    }
    return summary

if __name__ == "__main__":
    file = input("Log CSV: ")
    summary = analyze(file)
    print("\n=== SUMMARY ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
      
