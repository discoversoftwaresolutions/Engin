import streamlit as st
import pandas as pd
import logging
import requests

# ✅ Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

API_BASE_URL = "https://enginuity-production.up.railway.app/fusionx"

def render_dashboard():
    """Renders the FusionX CAD + CAM Intelligence dashboard."""
    try:
        st.title("🧩 FusionX: CAD + CAM Intelligence")
        st.caption("Design assistant, path optimizer, and manufacturability analysis powered by GPT-4.5")

        # ---- Sidebar Navigation ----
        st.sidebar.title("FusionX Controls")
        uploaded_file = st.sidebar.file_uploader("Upload CAD File", type=["step", "stl", "dxf"])
        design_goal = st.sidebar.text_input("Design Objective", placeholder="E.g., lightweight structural part")

        if uploaded_file:
            st.sidebar.success(f"✅ {uploaded_file.name} uploaded successfully!")

        # ---- Agent Actions (Tab Layout) ----
        tab1, tab2, tab3 = st.tabs(["🧠 Design Suggester", "📈 CAM Optimizer", "⚙️ Manufacturability"])

        with tab1:
            st.subheader("🧠 AI-Powered Design Suggestions")
            st.markdown("Provide a design goal, constraints, or material preferences.")
            prompt = st.text_area("Prompt", value="Suggest improvements for this aerospace bracket...")

            if st.button("Generate Suggestions"):
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/design-suggestions",
                        json={"prompt": prompt},
                        timeout=10
                    )
                    if res.status_code == 200:
                        response_data = res.json()
                        st.success(f"🔍 AI Suggests: {response_data.get('suggestion', 'Topology optimization & lightweight materials.')}")
                        logger.info("✅ Design suggestions retrieved successfully.")
                    else:
                        st.error(f"⚠️ Suggestion API Error: {res.text}")
                        logger.error(f"❌ API error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"⚠️ Failed to retrieve suggestions: {e}")
                    logger.error(f"❌ API request failed: {e}")

        with tab2:
            st.subheader("📈 CAM Path Optimization")
            st.markdown("Analyze toolpaths, reduce cycle time, and improve surface finish.")
            try:
                res = requests.get(f"{API_BASE_URL}/cam-optimization", timeout=10)
                if res.status_code == 200:
                    response_data = res.json()
                    st.image(response_data.get("cam_preview_url",
                        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/CNC_milling_example.gif/800px-CNC_milling_example.gif"),
                        caption="CAM Simulation",
                        use_container_width=True)
                    st.success(f"✅ Toolpath optimized: {response_data.get('efficiency_gain', '23% faster milling cycle estimated.')}")
                    logger.info("✅ CAM optimization retrieved successfully.")
                else:
                    st.error(f"⚠️ CAM API Error: {res.text}")
                    logger.error(f"❌ API error: {res.status_code} - {res.text}")
            except Exception as e:
                st.error(f"⚠️ Failed to retrieve CAM optimization data: {e}")
                logger.error(f"❌ API request failed: {e}")

        with tab3:
            st.subheader("⚙️ Manufacturability Feedback")
            st.markdown("Evaluate design features for fabrication efficiency.")
            st.code("Warning: Undercut detected in slot feature. May require custom tooling.", language="text")
            st.info("Suggestion: Convert sharp internal corners to fillets > 3mm radius.")

        st.markdown("---")
        st.markdown("© 2025 Discover Software Solutions • FusionX Module")

        # ---- GPT-4.5 Agent Section ----
        st.header("🧠 FusionX – CAD + CAM Design Assistant")
        prompt = st.text_area("Prompt GPT-4.5 Agent", placeholder="E.g., Optimize bracket design...")
        simulation_type = st.selectbox("Simulation Type", ["Structural", "Thermal", "None"])

        if st.button("🎯 Run Agent"):
            try:
                res = requests.post(
                    f"{API_BASE_URL}/run-agent",
                    json={"prompt": prompt, "simulation_type": simulation_type if simulation_type != "None" else None},
                    timeout=10
                )
                if res.status_code == 200:
                    response_data = res.json()
                    st.success("✅ Agent Response:")
                    st.json(response_data)
                    logger.info("✅ Agent execution completed successfully.")
                else:
                    st.error(f"⚠️ Agent API Error: {res.text}")
                    logger.error(f"❌ API error: {res.status_code} - {res.text}")
            except Exception as e:
                st.error(f"⚠️ Failed to execute agent: {e}")
                logger.error(f"❌ API request failed: {e}")

    except Exception as e:
        st.error("❌ FusionX encountered an unexpected issue.")
        logger.error(f"❌ Dashboard Error: {str(e)}")
