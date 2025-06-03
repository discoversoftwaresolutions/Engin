import streamlit as st
import pandas as pd
import logging
import requests

# ✅ Logger setup
logger = logging.getLogger(__name__)
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

API_BASE_URL = "https://enginuity-production.up.railway.app/fusionx"

def render_dashboard():
    """Renders the FusionX CAD + CAM Intelligence dashboard."""
    st.title("🧩 FusionX: CAD + CAM Intelligence")
    st.caption("Design assistant, path optimizer, and manufacturability analysis powered by GPT-4.5")

    # ---- Sidebar ----
    st.sidebar.title("FusionX Controls")
    uploaded_file = st.sidebar.file_uploader("📤 Upload CAD File", type=["step", "stl", "dxf"])
    design_goal = st.sidebar.text_input("🎯 Design Objective", placeholder="e.g. lightweight structural part")

    if uploaded_file:
        st.sidebar.success(f"✅ Uploaded: {uploaded_file.name}")

    # ---- Tabbed Interface ----
    tabs = st.tabs(["🧠 Design Suggester", "📈 CAM Optimizer", "⚙️ Manufacturability"])

    # --- Tab 1: Design Suggester ---
    with tabs[0]:
        st.subheader("🧠 AI-Powered Design Suggestions")
        prompt = st.text_area("Prompt", value="Suggest improvements for this aerospace bracket...")

        if st.button("Generate Suggestions"):
            try:
                res = requests.post(
                    f"{API_BASE_URL}/design-suggestions",
                    json={"prompt": prompt},
                    timeout=10
                )
                if res.status_code == 200:
                    suggestion = res.json().get("suggestion", "No suggestion returned.")
                    st.success(f"💡 Suggestion: {suggestion}")
                else:
                    raise ValueError(res.text)
            except Exception as e:
                st.error(f"⚠️ Failed to get suggestions: {e}")
                logger.exception("Design suggestion API failed")

    # --- Tab 2: CAM Optimizer ---
    with tabs[1]:
        st.subheader("📈 CAM Path Optimization")
        try:
            res = requests.get(f"{API_BASE_URL}/cam-optimization", timeout=10)
            if res.status_code == 200:
                data = res.json()
                cam_img = data.get("cam_preview_url")
                efficiency = data.get("efficiency_gain", "N/A")

                if cam_img:
                    st.image(cam_img, caption="CAM Simulation Preview", use_container_width=True)
                st.success(f"🛠 Efficiency Gain: {efficiency}")
            else:
                raise ValueError(res.text)
        except Exception as e:
            st.error(f"⚠️ CAM Optimization error: {e}")
            logger.exception("CAM optimization failed")

    # --- Tab 3: Manufacturability ---
    with tabs[2]:
        st.subheader("⚙️ Manufacturability Feedback")
        st.code("Warning: Undercut detected in slot feature. May require custom tooling.")
        st.info("Suggestion: Convert sharp internal corners to fillets > 3mm radius.")

    # --- Agent Assistant ---
    st.markdown("---")
    st.header("🧠 FusionX – CAD + CAM Design Assistant")

    agent_prompt = st.text_area("Prompt for GPT-4.5 Agent", placeholder="Optimize bracket design...")
    simulation_type = st.selectbox("Simulation Type", ["None", "Structural", "Thermal"])

    if st.button("🎯 Run Agent"):
        try:
            payload = {"prompt": agent_prompt}
            if simulation_type != "None":
                payload["simulation_type"] = simulation_type

            res = requests.post(f"{API_BASE_URL}/run-agent", json=payload, timeout=10)

            if res.status_code == 200:
                st.success("✅ Agent Response:")
                st.json(res.json())
            else:
                raise ValueError(res.text)
        except Exception as e:
            st.error(f"⚠️ Agent execution failed: {e}")
            logger.exception("Agent execution failed")

    st.markdown("© 2025 Discover Software Solutions • FusionX Module")
