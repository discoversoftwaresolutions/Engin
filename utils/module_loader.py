import importlib
import traceback
import sys
import os
import logging
import streamlit as st

logger = logging.getLogger(__name__)

def load_dynamic_module(module_path: str, fallback: callable = None):
    try:
        sys.path.insert(0, os.path.abspath("."))
        logger.info(f"📦 Importing {module_path}")
        module = importlib.import_module(module_path)
        return module
    except ModuleNotFoundError as e:
        logger.error(f"❌ Module not found: {e}")
        st.error(f"❌ Unable to load `{module_path}`.")
        if fallback:
            return fallback()
    except Exception as e:
        logger.error(f"🔥 Unexpected error: {e}")
        st.error(f"⚠ Error loading `{module_path}`.")
        st.code(traceback.format_exc(), language="python")
        if fallback:
            return fallback()
