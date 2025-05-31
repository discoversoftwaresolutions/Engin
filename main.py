import streamlit as st
import logging
import importlib
import sys
import os

# ✅ Configure Streamlit Page (Moved to the First Line)
st.set_page_config(
    page_title="Enginuity Agentic Suite",
    layout="wide",
    page_icon="🧠"
)

# ✅ Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✅ Dynamically add the correct path to the system
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.join(BASE_DIR, "modules")  # Adjust as needed
sys.path.append(MODULES_DIR)  # Ensure modules directory is added

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

# ---- Simplified Dynamic Import Handling ----
module_map = {
    "AeroIQ – Aerospace": "modules.aeroiq",
    "FlowCore – Digital Twin & Compliance": "modules.flowcore",
    "FusionX – Energy & Plasma": "modules.fusionx",
    "Simulai – Simulation AI": "modules.simulai",
    "VisuAI – Visual Intelligence": "modules.visuai",
    "ProtoPrint – Additive MFG": "modules.protoprint",
    "CircuitIQ – Electronics": "modules.circuitiq",
    "CodeMotion – Robotics Code": "modules.codemotion",
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
        import modules.aeroiq as fallback_module  # ✅ Fallback to AeroIQ
        fallback_module.render_dashboard()
except ModuleNotFoundError as e:
    logger.error(f"❌ Module `{module_name}` not found. Error: {e}")
    st.error(f"⚠ Module `{module_name}` not found. Ensure it exists and is properly configured.")
    import modules.aeroiq as fallback_module  # ✅ Fallback if module is missing
    fallback_module.render_dashboard()

# ---- Footer ----
st.markdown("---")
st.markdown("© 2025 Discover Software Solutions • All rights reserved.")
