import streamlit as st

st.set_page_config(page_title="Enginuity Unified Dashboard", layout="wide")

# ---- Header ----
st.markdown("## 🧠 Enginuity Unified Dashboard")
st.markdown("Agentic Engineering Suite powered by GPT-4.5 and proprietary algorithms")

# ---- Navigation Info ----
st.markdown("""
Welcome to **Enginuity** – a modular agentic engineering environment. Use the sidebar to access specific tools:
- **FusionX** for CAD + CAM design
- **SimulAI** for simulation tasks
- **VisuAI** for rendering & visualization
- **ProtoPrint** for additive manufacturing
- **CircuitIQ** for PCB layout and analysis
- **CodeMotion** for robotics and embedded systems
- **FlowCore** for lifecycle and digital twin management
""")

st.success("Navigate to a module using the sidebar menu.")
st.markdown("---")
st.markdown("© 2025 Discover Software Solutions • All rights reserved."
