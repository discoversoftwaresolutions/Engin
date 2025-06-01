import streamlit as st
import requests
import json
import logging

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="CircuitIQ – PCB & Supply Chain", layout="wide")

# ✅ Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("circuitiq")

# === Page Header ===
st.title("🧠 CircuitIQ – PCB Optimization & Supply Chain Intelligence")
st.markdown("Enhance circuit layouts, analyze power integrity, and check supply chain availability using intelligent agents.")

# === PCB Auto Layout Agent ===
st.subheader("🧩 Auto Layout Generator")
pcb_data = st.text_area("Upload Netlist / Schematic Data (JSON format)", value='{"components":[], "connections":[]}')

if st.button("Generate PCB Layout"):
    try:
        payload = json.loads(pcb_data)
    except json.JSONDecodeError:
        st.error("⚠️ Invalid JSON format. Please check your input.")
        logger.error("❌ JSON parsing error in PCB layout input.")
    else:
        try:
            res = requests.post("http://localhost:8000/circuitiq/auto-layout", json=payload)
            if res.status_code == 200:
                response_data = res.json()
                st.json(response_data)
                image_url = response_data.get("layout_preview_url", "https://fallback-image-url.com/default.png")
                st.image(image_url, caption="Generated PCB Layout", use_container_width=True)  # ✅ Dynamic preview
                logger.info("✅ PCB layout generated successfully.")
            else:
                st.error(f"⚠️ API Error: {res.status_code} - {res.text}")
                logger.error(f"❌ PCB layout API failed: {res.status_code} - {res.text}")
        except Exception as e:
            st.error(f"Failed to generate layout: {e}")
            logger.error(f"❌ PCB layout request failed: {e}")

# === Power Integrity Checker ===
st.markdown("---")
st.subheader("⚡ Power Integrity Checker")
pi_data = st.text_area("Input Voltage/Current Profile (JSON)", value='{"voltage":3.3,"current":0.8,"trace_width":0.5}')

if st.button("Check Power Integrity"):
    try:
        payload = json.loads(pi_data)
    except json.JSONDecodeError:
        st.error("⚠️ Invalid JSON format for power integrity input.")
        logger.error("❌ JSON parsing error in power integrity input.")
    else:
        try:
            res = requests.post("http://localhost:8000/circuitiq/power-integrity", json=payload)
            if res.status_code == 200:
                st.json(res.json())
                logger.info("✅ Power integrity check completed successfully.")
            else:
                st.error(f"⚠️ API Error: {res.status_code} - {res.text}")
                logger.error(f"❌ Power integrity API failed: {res.status_code} - {res.text}")
        except Exception as e:
            st.error(f"Power integrity check failed: {e}")
            logger.error(f"❌ Power integrity request failed: {e}")

# === Supply Chain Checker ===
st.markdown("---")
st.subheader("🚚 Supply Chain Availability")
bom = st.text_area("Bill of Materials (JSON)", value='[{"part":"LM317","available":false}]')

if st.button("Check Supply Chain"):
    try:
        payload = json.loads(bom)
    except json.JSONDecodeError:
        st.error("⚠️ Invalid JSON format for BOM input.")
        logger.error("❌ JSON parsing error in BOM input.")
    else:
        try:
            res = requests.post("http://localhost:8000/circuitiq/supply-chain", json=payload)
            if res.status_code == 200:
                result = res.json()
                st.json(result)
                logger.info("✅ Supply chain validation completed.")
            else:
                st.error(f"⚠️ API Error: {res.status_code} - {res.text}")
                logger.error(f"❌ Supply chain API failed: {res.status_code} - {res.text}")
        except Exception as e:
            st.error(f"Supply chain check failed: {e}")
            logger.error(f"❌ Supply chain request failed: {e}")

# ✅ Footer
st.markdown("---")
st.markdown("© 2025 Discover Software Solutions • CircuitIQ Module")
