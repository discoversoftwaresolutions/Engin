import streamlit as st

st.set_page_config(page_title="Enginuity - Unified Engineering Suite", layout="wide")

st.title("🧠 Enginuity Unified Engineering Dashboard")
st.caption("Agentic Engineering Suite powered by GPT-4.5 and proprietary algorithms")

# Intro Section
st.markdown("""
Enginuity combines advanced engineering tools with autonomous agents to accelerate design, simulation, compliance, and manufacturing.

This platform integrates modules for:
- 🧩 FusionX – CAD + CAM
- 🌊 SimulAI – Simulation (FEA/CFD)
- 🎨 VisuAI – Industrial Rendering
- 🧬 ProtoPrint – Additive Manufacturing
- 🔌 CircuitIQ – PCB Design
- 🤖 CodeMotion – Embedded + Robotics
- 🔄 FlowCore – Digital Twin + Compliance

Use the sidebar to explore each module or select below.
""")

# Navigation Buttons
cols = st.columns(3)
modules = {
    "FusionX (CAD + CAM)": "FusionX",
    "SimulAI (FEA/CFD)": "SimulAI",
    "VisuAI (Rendering)": "VisuAI",
    "ProtoPrint (3D Printing)": "ProtoPrint",
    "CircuitIQ (PCB)": "CircuitIQ",
    "CodeMotion (Robotics)": "CodeMotion",
    "FlowCore (Digital Twin)": "FlowCore"
    "AeroIQ (Aerospace)" 
}

for idx, (label, module) in enumerate(modules.items()):
    with cols[idx % 3]:
        st.page_link(f"/{module}", label=label, icon="🔗")

st.markdown("---")
st.markdown("© 2025 Discover Software Solutions • Built on GPT-4.5, Streamlit, and Railway Cloud")
