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

# Standard Lens Degree to Field Multiplier mapping
LENS_MULTIPLIERS = {
    "10° Lens (0.18)": 0.18,
    "14° Lens (0.25)": 0.25,
    "19° Lens (0.33)": 0.33,
    "26° Lens (0.46)": 0.46,
    "36° Lens (0.58)": 0.58,
    "50° Lens (0.93)": 0.93,
    "70° Lens (1.40)": 1.40,
    "90° Lens (2.00)": 2.00,
    "Other (Custom Multiplier)": None,
}

selected_lens = st.selectbox(
    "Lens Tube Size / Degree",
    options=list(LENS_MULTIPLIERS.keys()),
    index=4,  # Defaults to 36° Lens (0.58)
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

# Reference table expander
with st.expander("📊 Field Multiplier Reference Table"):
  st.markdown("""
    | Lens Degree | Field Multiplier |
    | :--- | :--- |
    | **10°** | 0.18 |
    | **14°** | 0.25 |
    | **19°** | 0.33 |
    | **26°** | 0.46 |
    | **36°** | 0.58 |
    | **50°** | 0.93 |
    | **70°** | 1.40 |
    | **90°** | 2.00 |
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
# Math Calculations (PowerPoint Logic)
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