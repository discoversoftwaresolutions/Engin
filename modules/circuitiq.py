# modules/circuitiq.py

import streamlit as st
import requests
import json

# ✅ This must be the first Streamlit command
st.set_page_config(page_title="CircuitIQ – PCB & Supply Chain", layout="wide")

# === Page Header ===
st.title("🧠 CircuitIQ – PCB Optimization & Supply Chain Intelligence")
st.markdown("Enhance circuit layouts, analyze power integrity, and check supply chain availability using intelligent agents.")

# === PCB Auto Layout Agent ===
st.subheader("🧩 Auto Layout Generator")
pcb_data = st.text_area("Upload Netlist / Schematic Data (JSON format)", value='{"components":[], "connections":[]}')
if st.button("Generate PCB Layout"):
    try:
        payload = json.loads(pcb_data)
        res = requests.post("http://localhost:8000/circuitiq/auto-layout", json=payload)
        st.json(res.json())
    except Exception as e:
        st.error(f"Failed to generate layout: {e}")

# === Power Integrity Checker ===
st.markdown("---")
st.subheader("⚡ Power Integrity Checker")
pi_data = st.text_area("Input Voltage/Current Profile (JSON)", value='{"voltage":3.3,"current":0.8,"trace_width":0.5}')
if st.button("Check Power Integrity"):
    try:
        payload = json.loads(pi_data)
        res = requests.post("http://localhost:8000/circuitiq/power-integrity", json=payload)
        st.json(res.json())
    except Exception as e:
        st.error(f"Power integrity check failed: {e}")

# === Supply Chain Checker ===
st.markdown("---")
st.subheader("🚚 Supply Chain Availability")
bom = st.text_area("Bill of Materials (JSON)", value='[{"part":"LM317","available":false}]')
if st.button("Check Supply Chain"):
    try:
        payload = json.loads(bom)
        res = requests.post("http://localhost:8000/circuitiq/supply-chain", json=payload)
        result = res.json()
        st.json(result)
    except Exception as e:
        st.error(f"Supply chain check failed: {e}")

# === Layout Preview (Optional Visualization) ===
st.markdown("---")
st.subheader("📐 Layout Preview")
image_url = "https://example.com/layout_preview.png"  # Replace with actual rendered image endpoint
st.image(image_url, caption="Generated PCB Layout", use_container_width=True)
