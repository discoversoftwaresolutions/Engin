from pathlib import Path
import streamlit as st
import requests
import logging
import json
from typing import Dict, Optional
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from modules.orbital_3d import plot_orbit_3d, get_live_satellite_position
from modules.orbital_sim import compute_orbit, compute_hohmann_transfer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_BASE_URL = "https://enginuity-production.up.railway.app/aeroiq"

def compute_wavefronts(mach: float, altitude_ft: float, num_points: int = 100):
    altitude_m = altitude_ft * 0.3048
    speed_of_sound = 343
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
            return
        st.success(f"✅ File '{file_name}' uploaded successfully.")

    if st.button("Run Task"):
        if not prompt.strip():
            st.warning("⚠️ Please provide a task description before running.")
            return
        try:
            files = {"file": uploaded_file.getvalue()} if uploaded_file else None
            payload = {"task": task, "prompt": prompt}
            res = requests.post(f"{API_BASE_URL}/run-task", json=payload, files=files, timeout=10)
            if res.status_code == 200:
                st.success("✅ Task Completed Successfully!")
                st.json(res.json())
            else:
                st.error(f"❌ Backend Error [{res.status_code}]: {res.text}")
        except Exception as e:
            st.error(f"❌ Internal Error: {str(e)}")

    with st.expander("💥 Supersonic Boom Visualization", expanded=False):
        st.markdown("Visualize how altitude and Mach number affect boom propagation and cutoff")
        col1, col2 = st.columns(2)
        mach = col1.slider("Mach Number", 1.0, 2.0, step=0.05, value=1.4)
        altitude = col2.slider("Altitude (ft)", 30000, 80000, step=5000, value=50000)
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

    with st.expander("🛰 Orbital Simulation", expanded=False):
        col1, col2, col3 = st.columns(3)
        sma = col1.slider("Semi-Major Axis (km)", 6578, 42000, step=100, value=8000)
        ecc = col2.slider("Eccentricity", 0.0, 0.9, step=0.01, value=0.2)
        inc = col3.slider("Inclination (°)", 0.0, 180.0, step=1.0, value=28.5)
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

    with st.expander("♻️ Hohmann Transfer Calculator", expanded=False):
        col1, col2 = st.columns(2)
        r1 = col1.number_input("Initial Orbit Radius (km)", min_value=6578, max_value=42000, value=7000)
        r2 = col2.number_input("Target Orbit Radius (km)", min_value=6578, max_value=42000, value=35786)
        if st.button("🧮 Compute Hohmann Transfer"):
            result = compute_hohmann_transfer(r1, r2)
            st.success(f"Δv1: {result['delta_v1_km_s']:.4f} km/s → Δv2: {result['delta_v2_km_s']:.4f} km/s")
            st.info(f"Total Δv: **{result['total_delta_v_km_s']:.4f} km/s**")
            st.info(f"Time of Flight: **{result['time_of_flight_min']:.2f} minutes**")

    st.markdown("---")
    st.markdown("© 2025 Discover Software Solutions • All rights reserved.")
"""

# Write to file
path = Path("/mnt/data/enginuity_frontend/modules/aeroiq.py")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(aeroiq_full_code)

str(path)
