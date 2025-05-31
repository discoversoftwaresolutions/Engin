import streamlit as st
import logging
from pages.aeroiq import render_aeroiq_dashboard
from pages.flowcore import render_flowcore_dashboard
from pages.fusionx import render_fusionx_dashboard
from pages.simulai import render_simulai_dashboard
from pages.visuai import render_visuai_dashboard
from pages.protoprint import render_protoprint_dashboard
from pages.circuitiq import render_circuitiq_dashboard
from pages.codemotion import render_codemotion_dashboard

# ✅ Setup logger properly
logger = logging.getLogger(__name__)

# ✅ Configure Streamlit Page
st.set_page_config(
    page_title="Enginuity Agentic Suite",
    layout="wide",
    page_icon="🧠"
)

# ---- Sidebar Navigation ----
st.sidebar.title("🧠 Enginuity Suite")
app_selection = st.sidebar.radio(
    "🔬 Select Engineering Module:",
    [
        "AeroIQ – Aerospace",
        "FlowCore – Digital Twin & Compliance",
        "FusionX – Energy & Plasma",
        "Simulai – Simulation AI",
        "VisuAI – Visual Intelligence",
        "ProtoPrint – Additive MFG",
        "CircuitIQ – Electronics",
        "CodeMotion – Robotics Code"
    ],
)

# ✅ Log selection
logger.info(f"User selected module: {app_selection}")

# ---- Route Logic ----
module_map = {
    "AeroIQ – Aerospace": render_aeroiq_dashboard,
    "FlowCore – Digital Twin & Compliance": render_flowcore_dashboard,
    "FusionX – Energy & Plasma": render_fusionx_dashboard,
    "Simulai – Simulation AI": render_simulai_dashboard,
    "VisuAI – Visual Intelligence": render_visuai_dashboard,
    "ProtoPrint – Additive MFG": render_protoprint_dashboard,
    "CircuitIQ – Electronics": render_circuitiq_dashboard,
    "CodeMotion – Robotics Code": render_codemotion_dashboard,
}

# ✅ Render selected module or fallback
if app_selection in module_map:
    module_map[app_selection]()
else:
    logger.warning(f"⚠ Unknown module selected: {app_selection}")
    st.warning("⚠ Unknown module selected. Loading default module...")
    render_aeroiq_dashboard()

# ---- Footer ----
st.markdown("---")
st.markdown("© 2025 Discover Software Solutions • All rights reserved.")
