# utils/module_registry.py

import importlib
import traceback
import os
import sys
import streamlit as st

def load_all_modules_from_dir(modules_path="modules"):
    """
    Scans a module directory and attempts to import each submodule.
    Returns a list of (module_name, status, error).
    """
    results = []

    # Make sure project root is in sys.path
    root_dir = os.path.abspath(".")
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

    # Get all subfolders in the modules/ directory
    try:
        module_names = [
            name for name in os.listdir(modules_path)
            if os.path.isdir(os.path.join(modules_path, name))
        ]
    except FileNotFoundError:
        st.error(f"❌ Directory `{modules_path}` not found.")
        return []

    for name in module_names:
        module_path = f"{modules_path}.{name}"
        try:
            importlib.import_module(module_path)
            results.append((module_path, "✅ Success", None))
        except Exception as e:
            results.append((module_path, "❌ Failed", traceback.format_exc()))

    return results

def display_module_registry():
    """
    Streamlit UI for displaying module load results.
    """
    st.markdown("# 📦 Module Registry Import Report")

    results = load_all_modules_from_dir()

    if not results:
        st.warning("No modules found or import attempts failed unexpectedly.")

    for module_path, status, error in results:
        st.markdown(f"### {module_path}")
        if status == "✅ Success":
            st.success(status)
        else:
            st.error(status)
            with st.expander("Show Error Traceback"):
                st.code(error, language="python")
        st.markdown("---")
