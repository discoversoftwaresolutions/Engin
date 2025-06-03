# module_loader.py

import importlib
import traceback
import sys
import os
import streamlit as st
import logging

logger = logging.getLogger(__name__)

def load_dynamic_module(module_path: str, fallback: callable = None):
    """
    Dynamically loads a Python module using importlib.

    Args:
        module_path (str): Full dotted module path, e.g., 'modules.aeroiq'.
        fallback (callable): Optional fallback function to call on failure.

    Returns:
        module: Imported module object if successful, or result of fallback.
    """
    try:
        # 🧠 Ensure project root is in sys.path for import resolution
        root_dir = os.path.abspath(".")
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)

        logger.info(f"📦 Attempting to import `{module_path}`")
        module = importlib.import_module(module_path)
        logger.info(f"✅ Successfully imported `{module_path}`")
        return module

    except ModuleNotFoundError as e:
        logger.error(f"❌ ModuleNotFoundError for `{module_path}`: {e}")
        st.error(f"❌ Unable to load `{module_path}`. Falling back.")
        if fallback:
            return fallback()
        return None

    except Exception as e:
        tb = traceback.format_exc()
        logger.exception(f"🔥 Unexpected error while importing `{module_path}`: {e}")
        st.error(f"⚠ Unexpected error occurred while loading `{module_path}`.")
        with st.expander("🔍 Technical Details"):
            st.code(tb, language="python")
        if fallback:
            return fallback()
        return None
