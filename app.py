import math
import streamlit as st

st.set_page_config(
    page_title="Stage Wash Calculator", page_icon="💡", layout="centered"
)

st.title("💡 Stage Wash Fixture Calculator")
st.write(
    "Calculate stage lighting areas and total fixtures using lens field"
    " multipliers."
)

# ---------------------------------------------------------
# Step 1: Determine Known Information
# ---------------------------------------------------------
st.subheader("1. Enter Stage & Fixture Info")

col_a, col_b = st.columns(2)

with col_a:
  stage_width = st.number_input(
      "Stage Width (ft)", min_value=1.0, value=24.0, step=1.0
  )

with col_b:
  distance = st.number_input(
      "Distance to Stage (ft)",
      min_value=1.0,
      value=20.0,
      step=1.0,
      help="Distance from truss to the top of the stage",
  )

# Fixture and Lens options based on official chart values[cite: 2]
LENS_MULTIPLIERS = {
    "Source Four 5° (0.12)": 0.12,
    "Source Four 10° (0.19)": 0.19,
    "Source Four 19° (0.31)": 0.31,
    "Source Four 26° (0.42)": 0.42,
    "Source Four 36° (0.58)": 0.58,
    "Source Four 50° (0.93)": 0.93,
    "Source 4 PARNel @ 25 Focus (0.46)": 0.46,
    "Source 4 PARNel @ 45 Focus (0.87)": 0.87,
    "Source 4 EA PAR - Very Narrow Spot / VNSP (0.32)": 0.32,
    "Source 4 EA PAR - Narrow Spot / NSP (0.33)": 0.33,
    "Source 4 EA PAR - Medium Flood / MFL (0.57)": 0.57,
    "Source 4 EA PAR - Wide Flood / WFL (0.89)": 0.89,
    "Other (Custom Multiplier)": None,
}

selected_lens = st.selectbox(
    "Luminaire / Lens Tube Size",
    options=list(LENS_MULTIPLIERS.keys()),
    index=4,  # Defaults to Source Four 36° (0.58)[cite: 2]
)

# Custom field multiplier fallback
if selected_lens == "Other (Custom Multiplier)":
  field_multiplier = st.number_input(
      "Enter Custom Field Multiplier",
      min_value=0.01,
      value=0.58,
      step=0.01,
      format="%.2f",
  )
else:
  field_multiplier = LENS_MULTIPLIERS[selected_lens]

# Reference table expander replicating the image chart[cite: 2]
with st.expander("📊 Photometric Reference Table (Field & Beam Multipliers)"):
  st.markdown("""
    | Luminaire | Focus | Field Angle | Beam Angle | Field Multiplier | Beam Multiplier |
    | :--- | :---: | :---: | :---: | :---: | :---: |
    | **Source Four 5°** | — | 7° | 5° | **0.12** | 0.09 |
    | **Source Four 10°** | — | 11° | 8° | **0.19** | 0.14 |
    | **Source Four 19°** | — | 17° | 14° | **0.31** | 0.25 |
    | **Source Four 26°** | — | 24° | 17° | **0.42** | 0.30 |
    | **Source Four 36°** | — | 33° | 23° | **0.58** | 0.41 |
    | **Source Four 50°** | — | 50° | 36° | **0.93** | 0.64 |
    | **Source 4 PARNel** | 25 | 26° | 12° | **0.46** | 0.21 |
    | **Source 4 PARNel** | 45 | 47° | 29° | **0.87** | 0.52 |
    | **Source 4 EA PAR** | VNSP | 18° | 11° | **0.32** | 0.19 |
    | **Source 4 EA PAR** | NSP | 19° | 11° | **0.33** | 0.19 |
    | **Source 4 EA PAR** | MFL | 32° | 19° | **0.57** | 0.33 |
    | **Source 4 EA PAR** | WFL | 48° | 27° | **0.89** | 0.47 |
    """)

# ---------------------------------------------------------
# Step 2: Overlap Percentage
# ---------------------------------------------------------
st.subheader("2. Stage Overlap")
overlap_pct = st.slider(
    "Target Overlap (%)", min_value=0, max_value=100, value=30, step=5
)
st.caption("📌 **NOTE:** Overlap is typically **30%**.")

# ---------------------------------------------------------
# Math Calculations
# ---------------------------------------------------------

# 1. Field of Light Produced = Distance * Field Multiplier
field_of_light = distance * field_multiplier

# 2. Total Area to Light = Stage Width * (1 + Overlap %)
total_area_to_light = stage_width * (1 + (overlap_pct / 100.0))

# 3. Areas to Light = Total Area / Field of Light (Rounded UP)
if field_of_light > 0:
  areas_needed = math.ceil(total_area_to_light / field_of_light)
else:
  areas_needed = 0

# 4. Total Fixtures = Areas * 2
total_fixtures = areas_needed * 2

st.divider()

# ---------------------------------------------------------
# Step 3: Calculation Results & Output
# ---------------------------------------------------------
st.subheader("3. Results")

res_col1, res_col2 = st.columns(2)

with res_col1:
  st.metric(label="Areas Needed to Light", value=f"{areas_needed} Areas")
  st.write(f"• **Field of Light Produced:** `{field_of_light:.2f} ft`")
  st.write(f"• **Total Area (w/ Overlap):** `{total_area_to_light:.2f} ft`")

with res_col2:
  st.metric(label="Total Fixtures Needed", value=f"{total_fixtures} Fixtures")
  st.info("💡 **NOTE:** You will need **2 lights** to light each area.")

# Full Step-by-Step Breakdown
with st.expander("🔍 View Step-by-Step Calculation Breakdown"):
  st.write(
      f"1. **Field of Light:** `{distance} ft × {field_multiplier} =`"
      f" **{field_of_light:.2f} ft**"
  )
  st.write(
      f"2. **Total Area to Light:** `{stage_width} ft ×`"
      f" `{(1 + (overlap_pct/100.0)):.2f} =` **{total_area_to_light:.2f} ft**"
  )
  st.write(
      f"3. **Areas Needed:** `{total_area_to_light:.2f} / {field_of_light:.2f}`"
      f" `= {total_area_to_light / field_of_light:.2f}` ➔ **{areas_needed}**"
      " (rounded up)"
  )
  st.write(
      f"4. **Amount of Fixtures:** `{areas_needed} areas × 2 lights =`"
      f" **{total_fixtures} total fixtures**"
  )