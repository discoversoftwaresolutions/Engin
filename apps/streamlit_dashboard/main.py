import streamlit as st
import logging
import importlib

# ✅ Setup logger properly
logging.basicConfig(level=logging.INFO)
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

# ---- Dynamic Import Handling ----
module_map = {
    "AeroIQ – Aerospace": "apps.streamlit_dashboard.pages.aeroiq",
    "FlowCore – Digital Twin & Compliance": "pages.flowcore",
    "FusionX – Energy & Plasma": "pages.fusionx",
    "Simulai – Simulation AI": "pages.simulai",
    "VisuAI – Visual Intelligence": "pages.visuai",
    "ProtoPrint – Additive MFG": "pages.protoprint",
    "CircuitIQ – Electronics": "pages.circuitiq",
    "CodeMotion – Robotics Code": "pages.codemotion",
}

if app_selection in module_map:
    try:
        module_name = module_map[app_selection]
        module = importlib.import_module(module_name)
        module.render_dashboard()  # ✅ Ensure each module implements `render_dashboard()`
    except ModuleNotFoundError as e:
        logger.error(f"❌ Failed to load module: {module_name}. Error: {e}")
        st.error(f"⚠ Module `{module_name}` not found. Ensure it exists and is properly configured.")
        render_aeroiq_dashboard()  # ✅ Fallback to AeroIQ
else:
    logger.warning(f"⚠ Unknown module selected: {app_selection}")
    st.warning("⚠ Unknown module selected. Loading default module...")
    render_aeroiq_dashboard()

# ---- Footer ----
st.markdown("---")
st.markdown("© 2025 Discover Software Solutions • All rights reserved.")
