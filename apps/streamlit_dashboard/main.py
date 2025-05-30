# apps/streamlit_dashboard/main.py

import streamlit as st
import os
import importlib.util

# ✅ Set global page config
st.set_page_config(page_title="Enginuity Engineering Suite", layout="wide")

# ✅ App Title
st.title("🧠 Enginuity Unified Engineering Dashboard")
st.markdown("Agentic Engineering Suite powered by GPT-4.5 and proprietary algorithms.")

# ✅ Dynamic module loading for all pages in ./pages
PAGES_DIR = os.path.join(os.path.dirname(__file__), "pages")
page_files = [f for f in os.listdir(PAGES_DIR) if f.endswith(".py")]

pages = {f.replace(".py", "").capitalize(): f for f in page_files}
selected_page = st.sidebar.selectbox("📁 Modules", list(pages.keys()))

# ✅ Load and execute selected module
page_file = os.path.join(PAGES_DIR, pages[selected_page])
spec = importlib.util.spec_from_file_location("module.name", page_file)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
