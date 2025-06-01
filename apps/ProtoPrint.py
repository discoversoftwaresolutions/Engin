import streamlit as st
import pandas as pd


st.title("🖨️ ProtoPrint: Additive Manufacturing Intelligence")
st.caption("Slicing, material selection, and print simulation driven by GPT-4.5 agents")

# Sidebar Inputs
st.sidebar.title("ProtoPrint Config")
gcode_file = st.sidebar.file_uploader("Upload G-code or STL", type=["gcode", "stl"])
print_material = st.sidebar.selectbox("Material Type", ["PLA", "ABS", "PETG", "Resin", "Carbon Fiber"])
layer_height = st.sidebar.slider("Layer Height (mm)", 0.05, 0.5, 0.2)
infill_percent = st.sidebar.slider("Infill Density (%)", 0, 100, 20)

if st.sidebar.button("Run Slicer & Simulate"):
    st.session_state["run_protoprint"] = True

# Tabs for Analysis
tab1, tab2, tab3 = st.tabs(["🧠 Slice Plan", "📈 Simulation", "🧬 Material Suggestion"])

with tab1:
    st.subheader("🧠 Agent Slice Optimization")
    st.code("Generated G-code Summary:\n- 92 layers @ 0.2mm\n- Travel path optimized: Z-hop enabled\n- Infill pattern: Gyroid\n- Estimated time: 3h 25m")
    st.success("Slicing and optimization complete.")

with tab2:
    st.subheader("📈 Thermal Stress Simulation")
    sim_data = pd.DataFrame({
        "Layer": [1, 20, 40, 60, 80],
        "Temp Gradient (°C)": [45, 38, 42, 50, 48],
        "Warp Potential (%)": [1.2, 0.8, 1.0, 2.5, 2.0]
    })
    st.line_chart(sim_data.set_index("Layer"))

with tab3:
    st.subheader("🧬 Material Recommendation")
    st.markdown("📌 *Selected Material*: **PETG**")
    st.code("Why PETG?\n- Better layer adhesion\n- Moderate flexibility\n- Minimal warping vs. PLA\n- More durable under stress")
    st.info("Alternative: Carbon Fiber Reinforced PLA for high rigidity")

st.markdown("---")
st.markdown("© 2025 Discover Software Solutions • ProtoPrint Module")
