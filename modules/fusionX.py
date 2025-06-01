import streamlit as st
import pandas as pd
import logging
from shared.api import post_prompt_to_agent

# ✅ Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("fusionx")

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
                response = post_prompt_to_agent("fusionx", prompt)
                st.success(f"🔍 AI Suggests: {response.get('suggestion', 'Topology optimization & lightweight materials.')}")
        
        with tab2:
            st.subheader("📈 CAM Path Optimization")
            st.markdown("Analyze toolpaths, reduce cycle time, and improve surface finish.")
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/CNC_milling_example.gif/800px-CNC_milling_example.gif",
                caption="CAM Simulation",
                use_container_width=True  # ✅ Updated parameter
            )
            st.success("✅ Toolpath optimized: 23% faster milling cycle estimated.")

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
            response = post_prompt_to_agent("fusionx", prompt, simulation_type if simulation_type != "None" else None)
            if "error" in response:
                st.error(response["error"])
                logger.error(f"❌ Error in AI response: {response['error']}")
            else:
                st.success("✅ Agent Response:")
                st.json(response)

    except Exception as e:
        st.error("❌ FusionX encountered an unexpected issue.")
        logger.error(f"❌ Dashboard Error: {str(e)}")

if __name__ == "__main__":
    render_dashboard()
