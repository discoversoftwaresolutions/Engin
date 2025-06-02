# app.py

import streamlit as st
import importlib
import logging

# ✅ Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enginuity-ui")

# ✅ Module registry
MODULES = {
    "🏁 Welcome": None,
    "🛩️ AeroIQ": "modules.aeroiq",
    "🎨 VisuAI": "modules.visuai",
    "🔧 CircuitIQ": "modules.circuitiq",
    "🧪 SimulAI": "modules.simulai",
    "🖨️ ProtoPrint": "modules.protoprint",
    "💡 CodeMotion": "modules.codemotion",
    "🌊 FlowCore": "modules.flowcore",
    "🔬 FusionX": "modules.fusionx"  # optional if present
}

# ✅ Sidebar menu
st.sidebar.title("🧠 Enginuity AI Suite")
choice = st.sidebar.radio("Choose a Module", list(MODULES.keys()))

# ✅ Main title
st.title("🚀 Enginuity Platform")
st.markdown("**Powered by Discover Software Solutions**")

# ✅ Load the selected module dynamically
if MODULES[choice]:
    try:
        module = importlib.import_module(MODULES[choice])
        module.render_dashboard()
    except ModuleNotFoundError as e:
        logger.warning(f"❌ Unable to load {MODULES[choice]}: {e}")
        st.error(f"Module not found: {MODULES[choice]}")
    except Exception as e:
        logger.exception(f"❌ Error in module {MODULES[choice]}")
        st.error(f"Failed to render {choice}. See logs.")
else:
    st.markdown("Welcome to **Enginuity**, your AI-powered engineering suite.")
    st.markdown("Use the sidebar to select a module.")

# ✅ Footer
st.markdown("---")
st.markdown("© 2025 Discover Software Solutions – All rights reserved.")
