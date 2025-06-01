import streamlit as st
import logging
import requests
from typing import Optional

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="VisuAI – Ergonomic & Visual Design", layout="wide")

# ✅ Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("visuai")

API_BASE_URL = "https://enginuity-production.up.railway.app/visuai"  # ✅ Integrated production endpoint

def render_dashboard():
    """Renders the VisuAI dashboard for photorealistic rendering and ergonomic evaluation."""

    st.title("🎨 VisuAI – Rendering & Ergonomic Design")
    st.markdown("Generate photorealistic renders, optimize product forms, and evaluate ergonomic fit in 3D environments.")

    # ✅ Model Upload Section
    uploaded_model = st.file_uploader("Upload 3D Model", type=["obj", "stl", "fbx"])

    if uploaded_model:
        model_name = uploaded_model.name
        file_size = uploaded_model.size / (1024 * 1024)  # Convert to MB

        if file_size > 50:
            st.error(f"⚠️ File too large ({file_size:.2f}MB). Please upload a file under 50MB.")
            logger.warning(f"❌ Model '{model_name}' exceeds allowed size limit.")
            return

        st.success(f"✅ Model '{model_name}' uploaded successfully.")
        logger.info(f"Model uploaded: {model_name} | Size: {file_size:.2f}MB")

        # ---- Rendering Controls ----
        render_style = st.selectbox("🎛 Rendering Style", ["Photorealism", "Sketch", "Wireframe"])

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🖼 Generate Render"):
                st.info(f"Rendering '{model_name}' in **{render_style}** mode...")
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/generate-render",
                        json={"filename": model_name, "style": render_style},
                        timeout=10
                    )
                    if res.status_code == 200:
                        response_data = res.json()
                        st.image(response_data.get("render_url", "https://fallback-image-url.com/default.png"),
                                 caption="Generated Render",
                                 use_container_width=True)  # ✅ Dynamically load render
                        st.success("✅ Render completed successfully.")
                        logger.info(f"✅ Render generated for '{model_name}' in '{render_style}' mode.")
                    else:
                        st.error(f"⚠️ Render failed: {res.text}")
                        logger.error(f"❌ Render API error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"⚠️ Rendering failed: {e}")
                    logger.error(f"❌ Render request failed: {e}")

        with col2:
            if st.button("🔍 Run Ergonomic Fit Evaluation"):
                st.info("Evaluating ergonomic posture and interaction...")
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/ergonomic-evaluation",
                        json={"model_name": model_name},
                        timeout=10
                    )
                    if res.status_code == 200:
                        st.success("✅ Ergonomic evaluation completed.")
                        logger.info("✅ Ergonomic evaluation successful.")
                    else:
                        st.error(f"⚠️ Evaluation failed: {res.text}")
                        logger.error(f"❌ Ergonomic API error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"⚠️ Ergonomic evaluation failed: {e}")
                    logger.error(f"❌ Ergonomic evaluation request failed: {e}")

        # ---- Agent Notes ----
        st.markdown("### 🧠 Render Agent Notes")
        st.text_area("Optional Notes", placeholder="Enter observations, ergonomic concerns, optimization insights...", height=150)

    # ---- Ergonomic Analysis Panel ----
    st.markdown("---")
    st.markdown("### 📏 Ergonomic Fit Parameters")

    percentile = st.slider("Anthropometric Percentile", min_value=1, max_value=99, value=50)
    show_stress_zones = st.checkbox("Highlight Ergonomic Stress Zones")

    if show_stress_zones:
        st.info("🟠 Highlighting high-stress ergonomic zones based on user interaction posture and geometry.")

    st.write(f"Selected percentile: {percentile}")
    logger.info(f"[VisuAI] Ergonomic config: Percentile={percentile}, ShowStress={show_stress_zones}")

if __name__ == "__main__":
    render_dashboard()
