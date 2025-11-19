import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Tree Pollution Reduction Simulator", layout="wide")

st.title("🌳 Tree-Based Pollution Reduction Simulator")
st.markdown("Learn how different trees reduce pollution and how many your community needs.")

# ------- Tree Data Table ------- #
tree_data = {
    "Tree Species": ["Oak", "Maple", "Cedar", "Pine", "Birch", "Dogwood"],
    "PM25_Removal_g_per_year": [15, 11, 18, 14, 8, 3],  # FIXED
    "CO2_kg_per_year": [30, 20, 25, 22, 12, 6],
    "Size": ["Large", "Medium", "Medium", "Medium", "Small", "Small"]
}

df_trees = pd.DataFrame(tree_data)

# -------- User Inputs -------- #
st.subheader("🌱 Select Trees and Placement")

species = st.selectbox("Choose Tree Species", df_trees["Tree Species"])
count = st.slider("Number of Trees", 1, 500, 50)

canopy_percent = st.slider("Estimated Canopy Coverage % of Neighborhood", 1, 60, 15)
years = st.slider("Growth Duration (years into the future)", 1, 20, 5)

# -------- Calculations -------- #
selected = df_trees[df_trees["Tree Species"] == species].iloc[0]

pm_reduced = selected["PM25_Removal_g_per_year"] * count
co2_reduced = selected["CO2_kg_per_year"] * count

# Growth multiplier (simple)
growth_factor = min(1, years / 10)
pm_reduced *= growth_factor
co2_reduced *= growth_factor

# Street-level air improvement
neighborhood_reduction = canopy_percent * 0.15  # %
neighborhood_reduction = min(neighborhood_reduction, 25)

# -------- Results -------- #
col1, col2 = st.columns(2)

with col1:
    st.metric("🌫 PM2.5 Removed / yr (grams)", f"{pm_reduced:,.0f}")
    st.metric("🌍 CO₂ Sequestered / yr (kg)", f"{co2_reduced:,.0f}")

with col2:
    st.metric("🏡 Neighborhood Air Quality Improvement (%)",
              f"{neighborhood_reduction:.1f}%")

# Visualization
st.subheader("📊 Pollution Removal Over Time")

years_list = np.arange(1, years+1)
growth_curve = np.minimum(1, years_list / 10)

pm_curve = selected["PM25_Removal_g_per_year"] * count * growth_curve
co2_curve = selected["CO2_kg_per_year"] * count * growth_curve

chart_df = pd.DataFrame({
    "Year": years_list,
    "PM2.5 Removed (g)": pm_curve,
    "CO2 Sequestered (kg)": co2_curve
})

st.line_chart(chart_df.set_index("Year"))

# Optional explanation
with st.expander("📘 How This Works"):
    st.write("""
    - Pollution removal values come from simplified community air-science models.  
    - Trees grow into full removal capacity over ~10 years.  
    - Canopy coverage directly changes neighborhood pollutant concentrations.  
    - This simulator is not a replacement for i-Tree Eco or i-Tree Planting, but a friendly educational tool.
    """)
