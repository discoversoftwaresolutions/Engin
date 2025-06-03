import streamlit as st
from utils.module_loader import load_dynamic_module
from utils.force_module_debug import force_load_module
from utils.module_registry import display_module_registry

st.title("🛠 Admin Debug Panel")

module_name = st.text_input("Module to Import (e.g., modules.aeroiq)")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔁 Load Module"):
        mod = load_dynamic_module(module_name)
        if mod:
            st.success(f"✅ Loaded: {module_name}")
with col2:
    if st.button("⚠ Force Debug Import"):
        force_load_module(module_name)
with col3:
    if st.button("🧹 Clear Streamlit Cache"):
        st.cache_resource.clear()
        st.success("✅ Cache cleared. Please reload manually.")

st.divider()

display_module_registry()
