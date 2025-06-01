import streamlit as st
import requests
import logging
from typing import Dict, Optional
import matplotlib.pyplot as plt
import numpy as np

# ✅ Setup Logger Properly
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE_URL = "https://enginuity-production.up.railway.app"  # ✅ Integrated production endpoint

# ✅ Supersonic Boom Physics Logic
def compute_wavefronts(mach: float, altitude_ft: float, num_points: int = 100):
    altitude_m = altitude_ft * 0.3048
    speed_of_sound = 343  # m/s at sea level
    aircraft_speed = mach * speed_of_sound

    angles = np.linspace(np.pi / 6, np.pi / 2.2, num_points)
    arc_radius = np.linspace(0, 20000, num_points)

    x_vals = arc_radius * np.cos(angles)
    y_vals = altitude_m - arc_radius * np.sin(angles)
    cutoff_altitude = altitude_m * 0.65

    return {
        "x": x_vals,
        "y": y_vals,
        "cutoff_altitude": cutoff_altitude,
        "altitude_m": altitude_m,
        "mach": mach
    }

# ✅ Main AeroIQ Render Function
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

    # 🔍 Supersonic Boom Visualization Section
    with st.expander("💥 Supersonic Boom Visualization", expanded=False):
        st.markdown("**Visualize how altitude and Mach number affect boom propagation and cutoff**")

        col1, col2 = st.columns(2)
        with col1:
            mach = st.slider("Mach Number", 1.0, 2.0, step=0.05, value=1.4)
        with col2:
            altitude = st.slider("Altitude (ft)", 30000, 80000, step=5000, value=50000)

        result = compute_wavefronts(mach, altitude)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(result["x"], result["y"], label="Wavefront Path", color="deepskyblue")
        ax.axhline(y=result["cutoff_altitude"], color="red", linestyle="--", label="Cutoff Altitude")
        ax.set_title(f"Supersonic Boom – Mach {mach} @ {altitude} ft")
        ax.set_xlabel("Horizontal Distance (m)")
        ax.set_ylabel("Altitude (m)")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

        st.info(f"✈️ Estimated cutoff altitude: **{result['cutoff_altitude']:.2f} meters**")

    st.markdown("---")
    st.markdown("© 2025 Discover Software Solutions • All rights reserved.")
