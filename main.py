
import streamlit as st
import logging
import importlib
import sys
import os
import traceback
import requests  # ✅ Used for backend API connectivity

# ========================
# 🔧 Streamlit Page Config
# ========================
st.set_page_config(
    page_title="Enginuity Agentic Suite",
    layout="wide",
    page_icon="🧠"
)

# ========================
# 📋 Logger Configuration
# ========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger("enginuity-main")

# ========================
# 🌐 API Configuration
# ========================
API_BASE_URL = "https://enginuity-production.up.railway.app"  # ✅ Defined before use

# ========================
# 🔁 Module Map (Ensuring Proper Order)
# ========================
module_map = {
    "Home": "modules.home",
    "AeroIQ - Aerospace": "module.aeroiq",
    "FlowCore - Digital Twin & Compliance": "modules.flowcore",
    "FusionX - Energy & Plasma": "moduel.fusionx",
    "Simulai - Simulation AI": "modules.simulai",
    "VisuAI - Visual Intelligence": "modules.visuai",
    "ProtoPrint - Additive MFG": "modules.protoprint",
    "CircuitIQ - Electronics": "modules.circuitiq",
    "CodeMotion - Robotics Code": "modules.codemotion",
}

# ========================
# 📌 Sidebar Navigation
# ========================
st.sidebar.title("🧠 Enginuity Suite")

routes = list(module_map.keys())  # ✅ Ensuring `module_map` exists before using it
app_selection = st.sidebar.radio("🔬 Select Engineering Module:", routes)

logger.info(f"📌 User selected: {app_selection}")

# ========================
# 📁 Ensure Module Pathing
# ========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

MODULES_DIR = os.path.join(BASE_DIR, "modules")
if MODULES_DIR not in sys.path:
    sys.path.insert(0, MODULES_DIR)

# ========================
# 🚨 Pre-load all modules to catch import errors early
# ========================
preload_modules = list(module_map.values())

for mod_name in preload_modules:
    try:
        importlib.import_module(mod_name)
        logger.info(f"✅ Preloaded: {mod_name}")
    except ModuleNotFoundError as e:
        logger.error(f"❌ Module not found during preload: {mod_name} | {e}")
        st.sidebar.error(f"❌ Failed to preload: `{mod_name}`")
    except Exception as e:
        logger.exception(f"🔥 Unexpected preload error for {mod_name}: {e}")
        st.sidebar.error(f"⚠ Error preloading `{mod_name}`: {str(e)}")

# ========================
# 🔌 API Status Check
# ========================
try:
    res = requests.get(f"{API_BASE_URL}/status", timeout=5)
    if res.status_code == 200:
        st.sidebar.success("✅ Connected to Enginuity API")
        logger.info("✅ API connection established successfully.")
    else:
        st.sidebar.warning("⚠️ API connection issue.")
        logger.warning(f"❌ API status error: {res.status_code} - {res.text}")
except requests.exceptions.RequestException as e:
    st.sidebar.warning("⚠️ Unable to connect to API.")
    logger.error(f"❌ API connection failed: {e}", exc_info=True)

# ========================
# 🔄 Dynamic Module Loader
# ========================
def load_module(module_key: str):
    """Dynamically loads selected engineering module."""
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
        tb = traceback.format_exc()
        logger.exception(f"🔥 Unexpected error while loading `{module_name}`: {e}")
        st.error(f"⚠ Unexpected error occurred while loading `{module_name}`.")
        with st.expander("🔍 Technical Details"):
            st.code(tb, language="python")
        fallback_to_home()

# ========================
# 🚨 Fallback Loader
# ========================
def fallback_to_home():
    """Fallback mechanism to load default Home module in case of failure."""
    try:
        import modules.home as fallback
        fallback.render_dashboard()
    except Exception as fallback_err:
        logger.critical(f"🚨 Fallback module `home` also failed: {fallback_err}")
        st.error("🚫 Critical error: Unable to load any dashboard modules.")
# main.py or app.py
from module_loader import load_dynamic_module
import streamlit as st

def fallback_to_home():
    st.warning("Redirecting to home module...")
    # Add your redirection logic here

# Load AeroIQ module
aeroiq_module = load_dynamic_module("modules.aeroiq", fallback=fallback_to_home)

# Example: Call a method in the module (if it loaded)
if aeroiq_module:
    try:
        aeroiq_module.render_dashboard()
    except Exception as e:
        st.error(f"Failed to render AeroIQ dashboard: {e}")
