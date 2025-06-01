import streamlit as st
import logging
import requests


# ✅ Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("codemotion")

API_BASE_URL = "https://enginuity-production.up.railway.app/codemotion"  # ✅ Integrated production endpoint

def render_dashboard():
    """Renders the CodeMotion dashboard for robotics and embedded systems development."""

    st.title("🤖 CodeMotion – Robotics & Embedded Systems")
    st.markdown("Generate embedded firmware, compose ROS2 behavior trees, and simulate robotic logic across platforms.")

    # ---- Platform Selection ----
    firmware_target = st.selectbox("🔧 Target Platform", ["ESP32", "STM32", "Arduino", "Raspberry Pi"])

    # ---- Code Upload ----
    uploaded_code = st.file_uploader("📂 Upload Hardware Specs / Code Snippet", type=["yaml", "json", "ino", "c", "cpp"])

    if uploaded_code:
        file_name = uploaded_code.name
        file_size = uploaded_code.size / (1024 * 1024)  # MB

        if file_size > 50:
            st.error(f"⚠️ File too large ({file_size:.2f}MB). Please upload a file under 50MB.")
            logger.warning(f"❌ Code file '{file_name}' exceeds allowed size limit.")
            return

        st.success(f"✅ '{file_name}' uploaded successfully.")
        logger.info(f"Code uploaded: {file_name} | Size: {file_size:.2f}MB")

        # ---- Action Buttons ----
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("⚙️ Generate Firmware"):
                st.info(f"Generating firmware for {firmware_target}...")
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/generate-firmware",
                        json={"filename": file_name, "platform": firmware_target},
                        timeout=10
                    )
                    if res.status_code == 200:
                        st.success("✅ Firmware generation completed!")
                        logger.info("✅ Firmware generated successfully.")
                    else:
                        st.error(f"⚠️ Firmware API Error: {res.text}")
                        logger.error(f"❌ API error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"⚠️ Firmware generation failed: {e}")
                    logger.error(f"❌ Firmware request failed: {e}")

        with col2:
            if st.button("🌐 Compose ROS2 Behavior Tree"):
                st.info(f"Composing ROS2 tree for {firmware_target}...")
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/compose-ros2",
                        json={"filename": file_name, "platform": firmware_target},
                        timeout=10
                    )
                    if res.status_code == 200:
                        st.success("✅ ROS2 behavior tree completed.")
                        logger.info("✅ ROS2 composition successful.")
                    else:
                        st.error(f"⚠️ ROS2 API Error: {res.text}")
                        logger.error(f"❌ API error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"⚠️ ROS2 composition failed: {e}")
                    logger.error(f"❌ ROS2 request failed: {e}")

        with col3:
            if st.button("🔄 Run Behavior Simulation"):
                st.info(f"Simulating behavior for {firmware_target}...")
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/simulate-behavior",
                        json={"filename": file_name, "platform": firmware_target},
                        timeout=10
                    )
                    if res.status_code == 200:
                        st.success("✅ Simulation completed.")
                        logger.info("✅ Behavior simulation successful.")
                    else:
                        st.error(f"⚠️ Simulation API Error: {res.text}")
                        logger.error(f"❌ API error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"⚠️ Simulation failed: {e}")
                    logger.error(f"❌ Simulation request failed: {e}")

        # ---- Code Agent Reasoning ----
        st.markdown("### 🧠 Code Agent Reasoning")
        st.text_area("Insights", placeholder="Enter performance insights, optimization reasoning...", height=200)

    # ---- Simulation Settings ----
    st.markdown("---")
    st.markdown("### 🎯 Simulation Settings")
    show_logs = st.checkbox("📜 Enable Detailed Execution Logs")
    show_metrics = st.checkbox("📊 Show Resource Utilization Metrics")

    if show_logs:
        st.info("📝 Execution logs will be generated for step-by-step traceability.")
    if show_metrics:
        st.info("📊 Memory, CPU, and storage metrics will be visualized.")

if __name__ == "__main__":
    render_dashboard()
