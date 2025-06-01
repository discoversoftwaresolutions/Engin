import streamlit as st
import logging
import importlib
from shared.config import module_map

"https://enginuity-production.up.railway.app"

# ✅ Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("enginuity-home")

# 🔁 Simulated Agent Status Check (replace with real pings or metrics later)
def check_agent_status(module_name: str) -> str:
    try:
        mod = importlib.import_module(module_name)
        return "🟢 Active" if hasattr(mod, "render_dashboard") else "🟡 Partial"
    except Exception:
        return "🔴 Offline"

def render_dashboard():
    """Renders the Enginuity Unified Dashboard with dynamic module listing and status indicators."""
    
    # ---- Hero Section ----
    st.markdown("## 🧠 Enginuity Unified Dashboard")
    st.markdown("### Agentic Engineering Intelligence Platform")
    st.write("Welcome to the unified control suite for engineering intelligence, simulation, and design powered by autonomous agents.")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.success("🚀 Explore CAD, CAM, digital twins, PCB layout, 3D print simulation, and ROS2 systems — all managed by intelligent engineering agents.")
    with col2:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Engineering_symbol.svg/2560px-Engineering_symbol.svg.png",
            use_container_width=True  # ✅ Updated parameter
        )

    st.divider()

    # ---- Module Overview ----
    st.markdown("### 🧩 Agentic Modules & Status")

    module_names = list(module_map.keys())
    half = len(module_names) // 2 + len(module_names) % 2
    col_a, col_b = st.columns(2)

    for idx, module_label in enumerate(module_names):
        mod = module_map[module_label]
        status = check_agent_status(mod)
        formatted = f"#### {module_label}  \nStatus: {status}"
        description = get_module_description(module_label)

        if idx < half:
            with col_a:
                st.markdown(formatted)
                st.caption(description)
        else:
            with col_b:
                st.markdown(formatted)
                st.caption(description)

    st.divider()

    # ---- Getting Started ----
    st.markdown("### 🧭 Getting Started")

    st.info("""
- **Step 1:** Select a module from the sidebar  
- **Step 2:** Upload your design file or describe the task  
- **Step 3:** Let Enginuity agents generate, simulate, and optimize your output  
""")

    st.markdown("> Need help? Visit documentation or contact support via the suite footer.")

    st.markdown("---")
    st.markdown("© 2025 **Discover Software Solutions** • Powered by the Discovery Platform.")

# 🔍 Descriptions for each module
def get_module_description(label: str) -> str:
    return {
        "AeroIQ – Aerospace": "Simulate CFD, optimize propulsion, and predict orbital mechanics.",
        "FlowCore – Digital Twin & Compliance": "Synchronize system states and verify engineering compliance.",
        "FusionX – Energy & Plasma": "Model energy systems and simulate plasma-driven processes.",
        "Simulai – Simulation AI": "High-fidelity physics and ML-driven simulation analysis.",
        "VisuAI – Visual Intelligence": "Photorealistic rendering and ergonomic evaluation.",
        "ProtoPrint – Additive MFG": "Prepare, slice, and simulate 3D print paths with material insight.",
        "CircuitIQ – Electronics": "PCB layout generation, power integrity checks, and vendor sourcing.",
        "CodeMotion – Robotics Code": "Compose firmware, ROS2 behavior, and run agentic robot tests."
    }.get(label, "Module description not available.")

if __name__ == "__main__":
    render_dashboard()
