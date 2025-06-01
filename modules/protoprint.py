import streamlit as st
import logging
import requests



# ✅ Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("protoprint")

API_BASE_URL = "https://enginuity-production.up.railway.app"  # ✅ Integrated production endpoint

def render_dashboard():
    """Renders the ProtoPrint dashboard for additive manufacturing simulation and material optimization."""

    st.title("🖨️ ProtoPrint – Additive Manufacturing")
    st.markdown("Simulate slicing paths, recommend materials, and evaluate print ergonomics for optimized additive workflows.")

    # ---- STL File Upload ----
    uploaded_stl = st.file_uploader("📂 Upload STL File", type=["stl"])
    
    if uploaded_stl:
        file_name = uploaded_stl.name
        file_size = uploaded_stl.size / (1024 * 1024)  # MB

        if file_size > 100:
            st.error(f"⚠️ File too large ({file_size:.2f}MB). Please upload a model under 100MB.")
            logger.warning(f"❌ STL file '{file_name}' exceeds allowed size limit.")
            return

        st.success(f"✅ '{file_name}' uploaded successfully.")
        logger.info(f"STL File: {file_name} | Size: {file_size:.2f}MB")

        # ---- Print Settings ----
        material = st.selectbox("🧪 Select Material", ["PLA", "ABS", "PETG", "Nylon", "Resin"])
        layer_height = st.slider("📏 Layer Height (mm)", min_value=0.05, max_value=0.3, value=0.1, step=0.01)

        # ---- Print Simulation Actions ----
        col1, col2 = st.columns(2)

        with col1:
            if st.button("📐 Simulate Print Path"):
                st.info(f"Simulating print path for '{file_name}' using {material} at {layer_height:.2f}mm...")
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/simulate-print-path",
                        json={"filename": file_name, "material": material, "layer_height": layer_height},
                        timeout=10
                    )
                    if res.status_code == 200:
                        response_data = res.json()
                        st.image(response_data.get("preview_url", "https://fallback-image-url.com/default.png"),
                                 caption="Simulated Print Path",
                                 use_container_width=True)  # ✅ Dynamically load preview
                        st.success("✅ Print path simulation completed.")
                        logger.info(f"✅ Print path simulated for '{file_name}' using '{material}' at {layer_height:.2f}mm.")
                    else:
                        st.error(f"⚠️ Simulation failed: {res.text}")
                        logger.error(f"❌ Print path API error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"⚠️ Print path simulation failed: {e}")
                    logger.error(f"❌ Print path request failed: {e}")

        with col2:
            if st.button("🔍 Run Material Recommendation"):
                st.info(f"Recommending material for '{file_name}' based on slicing constraints...")
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/recommend-material",
                        json={"filename": file_name, "layer_height": layer_height},
                        timeout=10
                    )
                    if res.status_code == 200:
                        response_data = res.json()
                        st.success(f"✅ Recommended Material: {response_data.get('recommended_material', 'No recommendation')}")
                        logger.info(f"✅ Material recommendation completed for '{file_name}'.")
                    else:
                        st.error(f"⚠️ Recommendation failed: {res.text}")
                        logger.error(f"❌ Material API error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"⚠️ Material recommendation failed: {e}")
                    logger.error(f"❌ Material recommendation request failed: {e}")

        # ---- Print Summary Notes ----
        st.markdown("### 🧠 Print Summary Notes")
        st.text_area("Summary / Observations", placeholder="E.g., Best results at 0.1mm layer height with PETG for overhangs...", height=200)

    # ---- Print Preview Settings ----
    st.markdown("---")
    st.markdown("### 📊 Print Preview Controls")

    show_temp_zones = st.checkbox("🌡️ Show Temperature Zones for Layer Fusion")
    enable_estimation = st.checkbox("⏱️ Enable Print Time Estimation")

    if show_temp_zones:
        st.info("🌡️ Visualizing thermal zones for layer fusion consistency.")

    if enable_estimation:
        st.info("⏱️ Estimating total print time based on selected settings.")

if __name__ == "__main__":
    render_dashboard()
