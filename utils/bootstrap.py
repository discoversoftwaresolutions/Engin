import sys
import os
import shutil
import streamlit as st
from pathlib import Path

def clear_pycache(root="."):
    """Recursively deletes all __pycache__ directories."""
    count = 0
    for pycache in Path(root).rglob("__pycache__"):
        try:
            shutil.rmtree(pycache)
            count += 1
        except Exception as e:
            st.warning(f"⚠ Could not remove {pycache}: {e}")
    return count

def scan_sys_modules():
    """Scans sys.modules for unexpected or typo'd module imports."""
    flagged = []
    for name in sorted(sys.modules.keys()):
        if any(sub in name for sub in ["moduel", "module.aeroiq", "moduel.fusionx", "fusionx", "aeroiq"]):
            flagged.append(name)
    return flagged

def verify_module_structure(base_path="modules"):
    """Checks that each folder in /modules is a valid Python package."""
    issues = []
    for sub in Path(base_path).iterdir():
        if sub.is_dir():
            init_file = sub / "__init__.py"
            if not init_file.exists():
                issues.append(f"Missing __init__.py in `{sub}`")
    return issues

def bootstrap_environment():
    """Run full environment sanity checks."""
    st.markdown("## 🧹 Environment Bootstrap")
    
    # 🔁 1. Clear __pycache__
    pycache_removed = clear_pycache()
    st.success(f"✅ Removed {pycache_removed} __pycache__ folders")

    # 👀 2. Scan sys.modules for ghosts
    ghost_modules = scan_sys_modules()
    if ghost_modules:
        st.error("❌ Detected stale or incorrect modules:")
        for mod in ghost_modules:
            st.code(mod)
    else:
        st.success("✅ No ghost modules detected in sys.modules")

    # 📦 3. Check module structure
    issues = verify_module_structure()
    if issues:
        st.warning("⚠ Issues with module package structure:")
        for msg in issues:
            st.write(f"- {msg}")
    else:
        st.success("✅ All modules are structured correctly with __init__.py")
