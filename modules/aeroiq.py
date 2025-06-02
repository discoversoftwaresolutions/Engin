import streamlit as st
import requests
import logging
from modules.orbital_3d import plot_orbit_3d, get_live_satellite_position
from typing import Dict, Optional
import matplotlib.pyplot as plt
import numpy as np
from modules.orbital_sim import compute_orbit, compute_hohmann_transfer
import plotly.graph_objects as go
from modules.orbital_sim import compute_orbit

# ✅ Setup Logger Properly
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE_URL = "https://enginuity-production.up.railway.app/aeroiq"  # ✅ Integrated production endpoint

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


# 🌌 Orbital Path Simulation
with st.expander("🛰 Orbital Simulation", expanded=False):
    st.markdown("**Visualize orbital mechanics based on classical orbital parameters.**")

    col1, col2, col3 = st.columns(3)
    with col1:
        sma = st.slider("Semi-Major Axis (km)", 6578, 42000, step=100, value=8000)
    with col2:
        ecc = st.slider("Eccentricity", 0.0, 0.9, step=0.01, value=0.2)
    with col3:
        inc = st.slider("Inclination (°)", 0.0, 180.0, step=1.0, value=28.5)

    x, y, meta = compute_orbit(semi_major_axis_km=sma, eccentricity=ecc, inclination_deg=inc)

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(x, y, color="lime", label="Orbital Path")
    ax.scatter([0], [0], color="blue", label="Earth Center", s=60)
    ax.set_aspect('equal')
    ax.set_xlabel("X (km)")
    ax.set_ylabel("Y (km)")
    ax.set_title("Keplerian Orbital Path")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    st.success(
        f"📍 Periapsis: **{meta['periapsis_km']:.2f} km** | "
        f"Apoapsis: **{meta['apoapsis_km']:.2f} km** | "
        f"Orbital Period: **{meta['orbital_period_min']:.2f} min**"
    )

# 🚀 Hohmann Transfer Calculator
with st.expander("♻️ Hohmann Transfer Calculator", expanded=False):
    st.markdown("Estimate delta-v and time-of-flight between two circular orbits.")

    col1, col2 = st.columns(2)
    with col1:
        r1 = st.number_input("Initial Orbit Radius (km)", min_value=6578, max_value=42000, value=7000)
    with col2:
        r2 = st.number_input("Target Orbit Radius (km)", min_value=6578, max_value=42000, value=35786)

    if st.button("🧮 Compute Hohmann Transfer"):
        result = compute_hohmann_transfer(r1, r2)
        st.success(f"Δv1: {result['delta_v1_km_s']:.4f} km/s → Δv2: {result['delta_v2_km_s']:.4f} km/s")
        st.info(f"Total Δv: **{result['total_delta_v_km_s']:.4f} km/s**")
        st.info(f"Time of Flight: **{result['time_of_flight_min']:.2f} minutes**")
        st.info(f"✈️ Estimated cutoff altitude: **{result['cutoff_altitude']:.2f} meters**")

def plot_orbit_3d(semi_major_axis_km, eccentricity, inclination_deg):
    x, y, meta = compute_orbit(semi_major_axis_km, eccentricity, inclination_deg)
    z = np.zeros_like(x)  # orbital plane

    # Rotate into inclined orbit in 3D
    inc_rad = np.radians(inclination_deg)
    z = y * np.sin(inc_rad)
    y = y * np.cos(inc_rad)

    # Earth Sphere
    u, v = np.mgrid[0:2*np.pi:50j, 0:np.pi:25j]
    xe = 6371 * np.cos(u) * np.sin(v)
    ye = 6371 * np.sin(u) * np.sin(v)
    ze = 6371 * np.cos(v)

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', name='Orbit Path', line=dict(color='lime')))
    fig.add_trace(go.Surface(x=xe, y=ye, z=ze, colorscale='Blues', opacity=0.6, showscale=False, name='Earth'))

    fig.update_layout(
        scene=dict(
            xaxis_title='X (km)', yaxis_title='Y (km)', zaxis_title='Z (km)',
            aspectmode='data',
        ),
        title='3D Orbital Visualization',
        height=700,
        showlegend=True
    )
    return fig
import streamlit as st
import requests
import json

st.markdown("## 🧠 Agentic Pipeline Executor")

# Define a simple default task pipeline
default_pipeline = [
    {
        "task_type": "predict_orbit",
        "payload": {"altitude_km": 400, "velocity_km_s": 7.66}
    },
    {
        "task_type": "optimize_nozzle",
        "payload": {"altitude": 30000, "diameter": 0.5}
    },
    {
        "task_type": "stress_analysis",
        "payload": {"material": "carbon", "load": 150}
    }
]

import streamlit as st
import requests
import json

st.markdown("## 🧠 Agentic Pipeline Executor")

# Define a simple default task pipeline
default_pipeline = [
    {
        "task_type": "predict_orbit",
        "payload": {"altitude_km": 400, "velocity_km_s": 7.66}
    },
    {
        "task_type": "optimize_nozzle",
        "payload": {"altitude": 30000, "diameter": 0.5}
    },
    {
        "task_type": "stress_analysis",
        "payload": {"material": "carbon", "load": 150}
    }
]

pipeline_json = st.text_area("📝 Define Your Task Pipeline (JSON)", value=json.dumps(default_pipeline, indent=2), height=300)

if st.button("🔁 Execute Task Pipeline"):
    try:
        parsed_pipeline = json.loads(pipeline_json)
        response = requests.post(
            "https://enginuity-production.up.railway.app/aeroiq/execute_pipeline",
            json={"pipeline": parsed_pipeline}
        )
        response.raise_for_status()
        st.success("✅ Pipeline executed successfully.")
        st.json(response.json())
    except json.JSONDecodeError:
        st.error("❌ Invalid JSON format. Please check your pipeline.")
    except requests.RequestException as e:
        st.error(f"🔥 API Error: {e}")

    st.markdown("---")
    st.markdown("© 2025 Discover Software Solutions • All rights reserved.")
