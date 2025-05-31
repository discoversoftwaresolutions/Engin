import streamlit as st
import logging
import importlib
import sys
import os

# ✅ Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Configure Streamlit Page
st.set_page_config(
    page_title="Enginuity Agentic Suite",
    layout="wide",
    page_icon="🧠"
)

# ✅ Dynamically add the correct path to the system
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "pages"))  # Adjust based on actual structure

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
    "AeroIQ – Aerospace": "pages.aeroiq",
    "FlowCore – Digital Twin & Compliance": "pages.flowcore",
    "FusionX – Energy & Plasma": "pages.fusionx",
    "Simulai – Simulation AI": "pages.simulai",
    "VisuAI – Visual Intelligence": "pages.visuai",
    "ProtoPrint – Additive MFG": "pages.protoprint",
    "CircuitIQ – Electronics": "pages.circuitiq",
    "CodeMotion – Robotics Code": "pages.codemotion",
}

# ✅ Load Selected Module or Fallback
try:
    if app_selection in module_map:
        module_name = module_map[app_selection]
        module = importlib.import_module(module_name)
        if hasattr(module, "render_dashboard"):  # Ensure function exists
            module.render_dashboard()
        else:
            logger.error(f"⚠ `{module_name}` does not have `render_dashboard()` function.")
            st.error(f"⚠ Module `{module_name}` missing `render_dashboard()`. Ensure correct implementation.")
    else:
        st.warning(f"⚠ Unknown module selected: {app_selection}")
        render_aeroiq_dashboard()  # ✅ Fallback to AeroIQ
except ModuleNotFoundError as e:
    logger.error(f"❌ Module `{module_name}` not found. Error: {e}")
    st.error(f"⚠ Module `{module_name}` not found. Ensure it exists and is properly configured.")
    render_aeroiq_dashboard()  # ✅ Fallback if module is missing

# ---- Footer ----
st.markdown("---")
st.markdown("© 2025 Discover Software Solutions • All rights reserved.")
