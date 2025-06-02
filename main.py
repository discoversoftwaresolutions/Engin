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
# 📁 Ensure Module Pathing
# ========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODULES_DIR = os.path.join(BASE_DIR, "modules")
if MODULES_DIR not in sys.path:
    sys.path.insert(0, MODULES_DIR)

# ========================
# 🌐 API Configuration
# ========================
API_BASE_URL = "https://enginuity-production.up.railway.app"

# ========================
# 📌 Sidebar Navigation
# ========================
st.sidebar.title("🧠 Enginuity Suite")

routes = [
    "Home",
    "AeroIQ - Aerospace",
    "FlowCore - Digital Twin & Compliance",
    "Simulai - Simulation AI",
    "FusionX - Energy & Plasma",
    "VisuAI - Visual Intelligence",
    "ProtoPrint - Additive MFG",
    "CircuitIQ - Electronics",
    "CodeMotion - Robotics Code"
]
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

app_selection = st.sidebar.radio("🔬 Select Engineering Module:", routes)

logger.info(f"📌 User selected: {app_selection}")

# ========================
# 🔁 Module Map (Updated for Root Modules)
# ========================
module_map = {
    "Home": "modules.home",
    "AeroIQ - Aerospace": "aeroiq",  # ✅ Adjusted for root directory
    "FlowCore - Digital Twin & Compliance": "modules.flowcore",
    "FusionX - Energy & Plasma": "fusionx",  # ✅ Adjusted for root directory
    "Simulai - Simulation AI": "modules.simulai",
    "VisuAI - Visual Intelligence": "modules.visuai",
    "ProtoPrint - Additive MFG": "modules.protoprint",
    "CircuitIQ - Electronics": "modules.circuitiq",
    "CodeMotion - Robotics Code": "modules.codemotion",
}

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
    except Exception
