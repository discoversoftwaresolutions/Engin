# force_module_debug.py

import importlib
import traceback
import sys
import os
import streamlit as st

def force_load_module(module_path: str):
    st.markdown(f"## 🔎 Forcing Load: `{module_path}`")
    
    # Show project path
    project_root = os.path.abspath(".")
    st.code(f"Project Root: {project_root}")
    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        st.info(f"✅ Injected `{project_root}` into sys.path")

    st.write("🔁 Current sys.path:")
    st.code("\n".join(sys.path))
    
    # Confirm module path physically exists
    module_folder = module_path.replace(".", "/")
    module_init = os.path.join(module_folder, "__init__.py")

    if os.path.exists(module_folder):
        st.success(f"✅ Folder exists: `{module_folder}`")
    else:
        st.error(f"❌ Folder not found: `{module_folder}`")

    if os.path.exists(module_init):
        st.success(f"✅ `__init__.py` exists: `{module_init}`")
    else:
        st.error(f"❌ Missing `__init__.py` at `{module_init}`")

    # Try import with full traceback
    try:
        st.markdown("### Attempting Import…")
        module = importlib.import_module(module_path)
        st.success(f"✅ Successfully imported `{module_path}`")
        return module
    except Exception as e:
        tb = traceback.format_exc()
        st.error(f"❌ Import failed: {e}")
        st.markdown("### Traceback:")
        st.code(tb, language="python")
        return None
