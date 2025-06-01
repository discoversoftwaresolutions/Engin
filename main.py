import streamlit as st
import logging
import importlib
import sys
import os

# ✅ Configure Streamlit Page FIRST
st.set_page_config(
    page_title="Enginuity Agentic Suite",
    layout="wide",
    page_icon="🧠"
)

# ✅ Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enginuity-main")

# ✅ Ensure modules path is included in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.join(BASE_DIR, "modules")
if MODULES_DIR not in sys.path:
    sys.path.insert(0, MODULES_DIR)

# ---- Sidebar Navigation ----
st.sidebar.title("🧠 Enginuity Suite")
app_selection = st.sidebar.radio(
    "🔬 Select Engineering Module:",
    [
        "Home",
        "AeroIQ – Aerospace",
        "FlowCore – Digital Twin & Compliance",
        "FusionX – Energy & Plasma",
        "Simulai – Simulation AI",
        "VisuAI – Visual Intelligence",
        "ProtoPrint – Additive MFG",
        "CircuitIQ – Electronics",
        "CodeMotion – Robotics Code"
    ],
    index=0  # Default selection is 'Home'
)

logger.info(f"📌 User selected: {app_selection}")

# ---- Module Mapping ----
module_map = {
    "Home": "modules.home",
    "AeroIQ – Aerospace": "modules.aeroiq",
    "FlowCore – Digital Twin & Compliance": "modules.flowcore",
    "FusionX – Energy & Plasma": "modules.fusionx",
    "Simulai – Simulation AI": "modules.simulai",
    "VisuAI – Visual Intelligence": "modules.visuai",
    "ProtoPrint – Additive MFG": "modules.protoprint",
    "CircuitIQ – Electronics": "modules.circuitiq",
    "CodeMotion – Robotics Code": "modules.codemotion",
}

# ---- Dynamic Module Loading ----
def load_module(module_key: str):
    module_name = module_map.get(module_key, "modules.home")
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, "render_dashboard"):
            module.render_dashboard()
        else:
            logger.error(f"🔧 `{module_name}` missing `render_dashboard()`.")
            st.error(f"⚠ `{module_name}` is missing the `render_dashboard()` function.")
            fallback_to_home()
    except ModuleNotFoundError as e:
        logger.error(f"❌ Failed to import `{module_name}`: {e}")
        st.error(f"❌ Unable to load `{module_name}`. Using fallback module.")
        fallback_to_home()
    except Exception as e:
        logger.exception(f"🔥 Unexpected error while loading module `{module_name}`: {e}")
        st.error("⚠ Unexpected error occurred while loading the module.")
        fallback_to_home()

# ---- Fallback Logic ----
def fallback_to_home():
    try:
        import modules.home as fallback
        fallback.render_dashboard()
    except Exception as fallback_err:
        logger.critical(f"🚨 Fallback module `home` also failed: {fallback_err}")
        st.error("🚫 Critical error: Unable to load any dashboard modules.")

# ---- Run Selected Module ----
load_module(app_selection)

# ---- Footer ----
st.markdown("---")
st.markdown("© 2025 **Discover Software Solutions** • All rights reserved.")
