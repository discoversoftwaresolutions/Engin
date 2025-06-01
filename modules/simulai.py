import streamlit as st
import pandas as pd
import logging
import requests

API_BASE_URL = "https://enginuity-production.up.railway.app" 


# ✅ Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("simulai")

def render_dashboard():
    """Renders the SimulAI dashboard with interactive simulation controls."""
    
    st.title("🧩 SimulAI: FEA / CFD / CAE Agent")
    st.caption("Run structural, thermal, and fluid simulations powered by GPT-4.5")

    # ---- Sidebar Controls ----
    st.sidebar.title("SimulAI Inputs")
    sim_file = st.sidebar.file_uploader("Upload Simulation Model", type=["step", "iges", "stl"])
    sim_type = st.sidebar.selectbox("Select Simulation Type", ["Structural", "Thermal", "Fluid", "Electromagnetic"])
    material = st.sidebar.text_input("Material", placeholder="e.g., Aluminum 6061-T6")

    if st.sidebar.button("Run Simulation"):
        if not sim_file:
            st.error("⚠️ Please upload a simulation model before running.")
            logger.warning("Simulation run attempted without a model file.")
        else:
            st.session_state["run_sim"] = True
            try:
                geometry_data = {"filename": sim_file.name, "material": material or "Unknown"}
                quality = "medium"
                res = requests.post(
                    "https://enginuity-production.up.railway.app/simulai/generate-mesh",
                    json={"geometry": geometry_data, "quality": quality},
                    timeout=10
                )
                logger.info(f"Mesh generation response: {res.status_code}")
                
                if res.status_code == 200:
                    response_data = res.json()
                    st.success("Mesh successfully generated.")
                    st.image(response_data.get("mesh_preview_url", "https://fallback-image-url.com/default.png"),
                             caption="Generated Mesh Preview",
                             use_container_width=True)  # ✅ Dynamically load image
                else:
                    st.error(f"⚠️ Mesh generation failed: {res.text}")
                    logger.error(f"❌ API Failure: {res.status_code} - {res.text}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Failed to contact SimulAI mesh API: {e}", exc_info=True)
                st.error("Could not connect to simulation backend.")

    # ---- Simulation Tabs ----
    tab1, tab2, tab3 = st.tabs(["🧠 Preprocessing", "📊 Simulation Output", "📋 Interpretation"])

    with tab1:
        st.subheader("🧠 Auto Mesh + Preprocessing")
        st.markdown("Meshing and boundary condition generation via GPT-4.5:")
        st.code("Mesh: 245,000 tetrahedral elements\nBCs: Fixed at base, load = 2.5kN at top face", language="text")
        st.success("Preprocessing completed.")

    with tab2:
        st.subheader("📊 Results")
        st.markdown("Visualize stress, temperature, or flow distribution:")
        
        result_data = pd.DataFrame({
            "Time (s)": [0, 1, 2, 3, 4, 5],
            "Max Stress (MPa)": [0, 75, 120, 150, 175, 180]
        })
        st.line_chart(result_data.set_index("Time (s)"))
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/4/4c/FEA_model_example.png",
            caption="Stress Distribution",
            use_container_width=True
        )

    with tab3:
        st.subheader("📋 AI Interpretation")
        st.markdown("Agentic interpretation of key insights from simulation results:")
        st.code("Max stress of 180 MPa observed at upper flange. Material yield = 260 MPa → PASS.")
        st.info("Recommendation: Add ribbing to reduce flex at base. Consider mesh refinement.")

    st.markdown("---")
    st.markdown("© 2025 Discover Software Solutions • SimulAI Module")

if __name__ == "__main__":
    render_dashboard()
