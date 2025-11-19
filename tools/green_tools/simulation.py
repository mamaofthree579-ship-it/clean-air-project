tools/green_tools/simulation.py
import pandas as pd
from pollutant_model import fleet_removal
import matplotlib.pyplot as plt

def simulate_fleet(species_key, count, years=30):
    df = fleet_removal(species_key, count, years=years)
    # cumulative sequestration
    df['cumulative_co2_kg'] = df['co2_kg'].cumsum()
    df['cumulative_pm_g'] = df['pm2_5_g'].cumsum()
    return df

def plot_simulation(df, species_key):
    fig, ax1 = plt.subplots(figsize=(8,4))
    ax1.plot(df['year'], df['cumulative_co2_kg'], label='Cumulative CO2 (kg)', color='green')
    ax1.set_ylabel('CO2 kg', color='green')
    ax2 = ax1.twinx()
    ax2.plot(df['year'], df['cumulative_pm_g'], label='Cumulative PM2.5 (g)', color='brown')
    ax2.set_ylabel('PM2.5 g', color='brown')
    ax1.set_xlabel('Year')
    ax1.set_title(f"Multi-year simulation: {species_key}")
    fig.tight_layout()
    return fig

if __name__ == "__main__":
    df = simulate_fleet("quercus_robur", 50, years=30)
    fig = plot_simulation(df, "quercus_robur")
    fig.savefig("simulation.png")
    print("Saved simulation.png")
  
