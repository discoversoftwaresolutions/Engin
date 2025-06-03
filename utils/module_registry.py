import importlib
import os
import traceback
import sys
import streamlit as st

def force_load_module(module_path: str):
    st.markdown(f"## 🔍 Forcing Import: `{module_path}`")
    root_dir = os.path.abspath(".")
    sys.path.insert(0, root_dir)

    folder = module_path.replace(".", "/")
    init_file = os.path.join(folder, "__init__.py")

    st.code(f"sys.path: {root_dir}")
    if os.path.exists(folder):
        st.success(f"✅ Folder exists: {folder}")
    else:
        st.error(f"❌ Folder not found: {folder}")

    if os.path.exists(init_file):
        st.success(f"✅ Found: {init_file}")
    else:
        st.warning(f"⚠ Missing __init__.py")

    try:
        mod = importlib.import_module(module_path)
        st.success("✅ Import successful")
        return mod
    except Exception as e:
        st.error(f"❌ Import failed: {e}")
        st.code(traceback.format_exc())
