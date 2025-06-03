import streamlit as st
import logging
import importlib
import sys
import os
import traceback
import requests

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
API_BASE_URL = "https://enginuity-production.up.railway.app"

# ========================
# 🧭 Module Map (Routing)
# ========================
module_map = {
    "Home": "modules.home",
    "AeroIQ - Aerospace": "modules.aeroiq",
    "FlowCore - Digital Twin & Compliance": "modules.flowcore",
    "FusionX - Energy & Plasma": "modules.fusionx",  # ✅ fixed typo
    "Simulai - Simulation AI": "modules.simulai",
    "VisuAI - Visual Intelligence": "modules.visuai",
    "ProtoPrint - Additive MFG": "modules.protoprint",
    "CircuitIQ - Electronics": "modules.circuitiq",
    "CodeMotion - Robotics Code": "modules.codemotion",
}

# ========================
# 📁 Ensure Module Paths
# ========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(BASE_DIR, "app")
MODULES_DIR = os.path.join(BASE_DIR, "modules")

for path in [APP_DIR, MODULES_DIR, BASE_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

# ========================
# 📌 Sidebar Navigation
# ========================
st.sidebar.title("🧠 Enginuity Suite")
routes = list(module_map.keys())
app_selection = st.sidebar.radio("🔬 Select Engineering Module:", routes)
logger.info(f"📌 User selected: {app_selection}")

# ========================
# 🔌 API Health Check
# ========================
try:
    res = requests.get(f"{API_BASE_URL}/status", timeout=5)
    if res.status_code == 200:
        st.sidebar.success("✅ Connected to Enginuity API")
    else:
        st.sidebar.warning("⚠️ API issue detected.")
except requests.exceptions.RequestException as e:
    st.sidebar.warning("⚠️ Unable to connect to API.")
    logger.error(f"❌ API connection failed: {e}", exc_info=True)

# ========================
# 🚨 Preload Module Imports
# ========================
for mod_name in module_map.values():
    try:
        importlib.import_module(mod_name)
        logger.info(f"✅ Preloaded: {mod_name}")
    except ModuleNotFoundError as e:
        logger.error(f"❌ Module not found during preload: {mod_name} | {e}")
        st.sidebar.error(f"❌ Failed to preload: `{mod_name}`")
    except Exception as e:
        logger.exception(f"🔥 Unexpected preload error for {mod_name}: {e}")
        st.sidebar.error(f"⚠ Error preloading `{mod_name}`")

# ========================
# 🔄 Fallback Loader
# ========================
def fallback_to_home():
    try:
        import modules.home as fallback
        fallback.render_dashboard()
    except Exception as fallback_err:
        tb = traceback.format_exc()
        logger.critical(f"🚨 Fallback failed: {fallback_err}")
        st.error("🚫 Critical error: Unable to load any module.")
        with st.expander("Error Details"):
            st.code(tb, language="python")

# ========================
# 📦 Dynamic Module Loader
# ========================
def load_module(module_key: str):
    module_name = module_map.get(module_key, "modules.home")
    try:
        module = importlib.import_module(module_name)
        if hasattr(module, "render_dashboard"):
            module.render_dashboard()
        else:
            st.error(f"⚠ `{module_name}` lacks `render_dashboard()`")
            logger.warning(f"🔧 Missing render_dashboard() in {module_name}")
            fallback_to_home()
    except ModuleNotFoundError as e:
        logger.error(f"❌ Module `{module_name}` not found: {e}")
        st.error(f"❌ Could not load `{module_name}`. Redirecting...")
        fallback_to_home()
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"🔥 Unexpected error in `{module_name}`: {e}")
        st.error(f"⚠ Error loading `{module_name}`.")
        with st.expander("🔍 Technical Details"):
            st.code(tb, language="python")
        fallback_to_home()

# ========================
# 🚀 Launch Selected Module
# ========================
load_module(app_selection)

# ========================
# 🧪 Optional Debug Info
# ========================
if st.sidebar.checkbox("🔍 Show Loaded Modules"):
    st.markdown("### Loaded sys.modules")
    for name in sorted(sys.modules.keys()):
        if any(x in name for x in ["aeroiq", "fusionx", "modules"]):
            st.code(name)
