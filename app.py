import math
import streamlit as st

st.set_page_config(
    page_title="Stage Wash Calculator", page_icon="💡", layout="centered"
)

st.title("💡 Stage Wash Fixture Calculator")
st.write("Calculate required fixtures and spacing for even stage coverage.")

# Input Section
st.subheader("1. Enter Parameters")
col1, col2 = st.columns(2)

with col1:
  stage_width = st.number_input(
      "Stage Width (ft)", min_value=1.0, value=40.0, step=1.0
  )
  distance = st.number_input(
      "Throw Distance / Trim Height (ft)",
      min_value=1.0,
      value=15.0,
      step=1.0,
  )

with col2:
  beam_angle = st.number_input(
      "Fixture Field Angle (°)",
      min_value=1.0,
      max_value=180.0,
      value=30.0,
      step=1.0,
  )
  overlap_pct = (
      st.slider(
          "Target Overlap (%)", min_value=0, max_value=60, value=30, step=5
      )
      / 100.0
  )

# Math Logic
rad = math.radians(beam_angle)
pool_width = 2 * distance * math.tan(rad / 2)
effective_coverage = pool_width * (1 - overlap_pct)

if stage_width <= pool_width:
  fixtures = 1
  spacing = 0.0
else:
  fixtures = math.ceil(1 + ((stage_width - pool_width) / effective_coverage))
  spacing = stage_width / (fixtures - 1) if fixtures > 1 else 0.0

st.divider()

# Output Section
st.subheader("2. Results")
st.metric(label="Fixtures Needed Per Pipe/Bar", value=f"{fixtures} Fixtures")

col_a, col_b = st.columns(2)
with col_a:
  st.info(f"**Individual Pool Diameter:**\n\n{pool_width:.1f} ft")
with col_b:
  if fixtures > 1:
    st.success(f"**Center-to-Center Spacing:**\n\n~{spacing:.1f} ft")
  else:
    st.success("**Center-to-Center Spacing:**\n\n1 fixture covers full width")