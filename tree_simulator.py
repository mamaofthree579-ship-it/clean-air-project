import streamlit as st
import pandas as pd
import numpy as np

# ---------------------------#
#      PAGE CONFIG SETUP
# ---------------------------#
st.set_page_config(
    page_title="Tree Pollution Reduction Simulator",
    layout="wide",
    page_icon="🌳"
)

# ---------------------------#
#         HEADER
# ---------------------------#
st.title("🌳 Tree-Based Pollution Reduction Simulator")
st.markdown("""
Use this tool to estimate how different tree species help reduce air pollution in your community.  
Values are simplified, educational, and scale with tree growth.
""")

st.divider()

# ---------------------------#
#      TREE DATA TABLE
# ---------------------------#
tree_data = {
    "Tree Species": [
        "Oak", "Maple", "Cedar", "Pine", "Birch", "Dogwood",
        "Spruce", "Sycamore", "Willow", "Poplar"
    ],
    "PM25_Removal_g_per_year": [15, 11, 18, 14, 8, 3, 20, 17, 13, 9],
    "CO2_kg_per_year":         [30, 20, 25, 22, 12, 6, 28, 24, 21, 10],
    "Size": [
        "Large", "Medium", "Medium", "Medium", "Small", "Small",
        "Large", "Large", "Large", "Medium"
    ]
}

df_trees = pd.DataFrame(tree_data)

# ---------------------------#
#     SIDEBAR INPUTS
# ---------------------------#
with st.sidebar:
    st.header("🌱 Select Tree Plan")

    species = st.selectbox("Tree Species", df_trees["Tree Species"])

    count = st.slider("Number of Trees", 1, 500, 50)

    canopy_percent = st.slider(
        "Neighborhood Canopy Coverage (%)",
        1, 60, 15
    )

    years = st.slider(
        "Growth Duration (years into the future)",
        1, 25, 10
    )

    st.markdown("---")
    show_table = st.checkbox("Show full tree data table", value=False)

# ---------------------------#
#       CALCULATIONS
# ---------------------------#
selected = df_trees[df_trees["Tree Species"] == species].iloc[0]

pm_base = selected["PM25_Removal_g_per_year"]
co2_base = selected["CO2_kg_per_year"]

# Growth model — full size at year 10
growth_factor = np.clip(years / 10, 0.1, 1.0)

pm_reduced = pm_base * count * growth_factor
co2_reduced = co2_base * count * growth_factor

# Neighborhood improvement model
neighborhood_reduction = min(canopy_percent * 0.15, 25)

# ---------------------------#
#         OUTPUT CARDS
# ---------------------------#
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌫 PM2.5 Removed / yr (grams)", f"{pm_reduced:,.0f}")

with col2:
    st.metric("🌍 CO₂ Sequestered / yr (kg)", f"{co2_reduced:,.0f}")

with col3:
    st.metric("🏡 Neighborhood AQ Improvement (%)",
              f"{neighborhood_reduction:.1f}%")


st.divider()

# ---------------------------#
#      CHART VISUALIZATION
# ---------------------------#
st.subheader("📊 Pollution Removal Over Time")

years_list = np.arange(1, years + 1)
growth_curve = np.clip(years_list / 10, 0.1, 1.0)

chart_df = pd.DataFrame({
    "Year": years_list,
    "PM2.5 Removed (g)": pm_base * count * growth_curve,
    "CO2 Sequestered (kg)": co2_base * count * growth_curve
}).set_index("Year")

st.line_chart(chart_df)

# ---------------------------#
#      OPTIONAL TABLE VIEW
# ---------------------------#
if show_table:
    st.subheader("🌳 Full Tree Data Table")
    st.dataframe(df_trees, use_container_width=True)

# ---------------------------#
#         INFO EXPANDER
# ---------------------------#
with st.expander("📘 How This Works"):
    st.write("""
### Tree Removal Estimates  
These values represent approximate **annual pollution removal** once the tree reaches maturity.  
Growth is estimated linearly for educational purposes.

### PM2.5 Reduction  
Small particulates removed through:  
- leaf surface adhesion  
- filtering during rainfall  
- canopy shading reducing local emissions

### CO₂ Sequestration  
Organic carbon storage increases over the lifespan of the tree.

### Neighborhood Air Quality  
A simplified canopy-density multiplier estimates local effects — not a substitute for i-Tree Eco.
    """)
