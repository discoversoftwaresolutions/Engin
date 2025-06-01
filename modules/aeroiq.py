import streamlit as st
import requests
import logging
from typing import Dict, Optional

# ✅ Setup Logger Properly
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE_URL = "https://enginuity-production.up.railway.app"  # ✅ Integrated production endpoint

def render_dashboard():
    st.title("🚀 AeroIQ - Aerospace Engineering Module")
    st.markdown("Model-based systems engineering, propulsion, avionics, and orbital simulation.")

    task_options = {
        "CFD Solver": "Computational fluid dynamics simulation.",
        "Propulsion Optimizer": "Optimizing propulsion systems.",
        "Structural Analysis": "Evaluate airframe stress and reliability.",
        "Orbital Prediction": "Simulate satellite orbits and trajectories.",
        "System Integration": "Verify system architecture dependencies.",
        "Quantum Payload Optimization": "Optimize payload using quantum algorithms.",
        "Firmware Build": "Generate embedded firmware.",
        "Regulatory Compliance": "Assess engineering compliance."
    }

    task = st.sidebar.selectbox("Select Task", list(task_options.keys()))
    st.sidebar.markdown(f"ℹ **Task Description:** {task_options[task]}")

    st.subheader(f"🛠️ Task: {task}")
    prompt = st.text_area("Describe your objective", placeholder="E.g., Optimize nozzle design for supersonic cruise...")

    uploaded_file = st.file_uploader("Upload Design/Data File", type=["json", "csv", "stl", "txt"])

    if uploaded_file:
        file_name = uploaded_file.name
        file_size = uploaded_file.size / (1024 * 1024)
        if file_size > 50:
            st.error(f"⚠ File too large ({file_size:.2f}MB). Please upload a file under 50MB.")
            logger.warning(f"❌ File '{file_name}' exceeds allowed size limit.")
            return

        st.success(f"✅ File '{file_name}' uploaded successfully.")
        logger.info(f"File uploaded: {file_name} | Size: {file_size:.2f}MB")

    if st.button("Run Task"):
        if not prompt.strip():
            st.warning("⚠️ Please provide a task description before running.")
            return

        st.info("⏳ Running task... Please wait.")
        try:
            files = {"file": uploaded_file.getvalue()} if uploaded_file else None
            payload = {"task": task, "prompt": prompt}

            res = requests.post(f"{API_BASE_URL}/run-task", json=payload, files=files, timeout=10)
            if res.status_code == 200:
                result = res.json()
                st.success("✅ Task Completed Successfully!")
                st.json(result)
                logger.info(f"Task '{task}' executed successfully with prompt: {prompt}")
            else:
                st.error(f"❌ Backend Error [{res.status_code}]: {res.text}")
                logger.error(f"API Error: {res.status_code} | Response: {res.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ API Request Failed: {str(e)}")
            logger.error(f"Exception during API request: {e}", exc_info=True)

        except Exception as e:
            st.error(f"❌ Internal Error: {str(e)}")
            logger.error(f"Exception during task execution: {e}", exc_info=True)

    st.markdown("---")
    st.markdown("© 2025 Discover Software Solutions • All rights reserved.")
