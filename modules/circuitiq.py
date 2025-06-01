import streamlit as st
import requests
import json
import logging

# ✅ Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("circuitiq")

API_BASE_URL = "https://enginuity-production.up.railway.app"  # ✅ Integrated production endpoint

def render_dashboard():
    """Renders the CircuitIQ – PCB Optimization & Supply Chain Intelligence dashboard."""
    
    st.title("🧠 CircuitIQ – PCB Optimization & Supply Chain Intelligence")
    st.markdown("Enhance circuit layouts, analyze power integrity, and check supply chain availability using intelligent agents.")

    # === PCB Auto Layout Agent ===
    st.subheader("🧩 Auto Layout Generator")
    pcb_data = st.text_area("Upload Netlist / Schematic Data (JSON format)", value='{"components":[], "connections":[]}')
    
    if st.button("Generate PCB Layout"):
        try:
            payload = json.loads(pcb_data)
            res = requests.post(f"{API_BASE_URL}/auto-layout", json=payload, timeout=10)
            if res.status_code == 200:
                st.json(res.json())
                logger.info("✅ PCB layout generated successfully.")
            else:
                st.error(f"⚠️ Layout API Error: {res.text}")
                logger.error(f"❌ API error: {res.status_code} - {res.text}")
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
            res = requests.post(f"{API_BASE_URL}/power-integrity", json=payload, timeout=10)
            if res.status_code == 200:
                st.json(res.json())
                logger.info("✅ Power integrity check completed successfully.")
            else:
                st.error(f"⚠️ Power Integrity API Error: {res.text}")
                logger.error(f"❌ API error: {res.status_code} - {res.text}")
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
            res = requests.post(f"{API_BASE_URL}/supply-chain", json=payload, timeout=10)
            if res.status_code == 200:
                result = res.json()
                st.json(result)
                logger.info("✅ Supply chain validation completed successfully.")
            else:
                st.error(f"⚠️ Supply Chain API Error: {res.text}")
                logger.error(f"❌ API error: {res.status_code} - {res.text}")
        except Exception as e:
            st.error(f"Supply chain check failed: {e}")
            logger.error(f"❌ Supply chain request failed: {e}")

    # === Layout Preview (Optional Visualization) ===
    st.markdown("---")
    st.subheader("📐 Layout Preview")
    
    try:
        res = requests.get(f"{API_BASE_URL}/layout-preview", timeout=10)
        if res.status_code == 200:
            image_url = res.json().get("preview_url", "https://fallback-image-url.com/default.png")
            st.image(image_url, caption="Generated PCB Layout", use_container_width=True)  # ✅ Dynamically load preview
            logger.info("✅ Layout preview retrieved successfully.")
        else:
            st.error(f"⚠️ Layout Preview API Error: {res.text}")
            logger.error(f"❌ API error: {res.status_code} - {res.text}")
    except Exception as e:
        st.error(f"⚠️ Failed to retrieve layout preview: {e}")
        logger.error(f"❌ Layout preview request failed: {e}")

    # ✅ Footer
    st.markdown("---")
    st.markdown("© 2025 Discover Software Solutions • CircuitIQ Module")

if __name__ == "__main__":
    render_dashboard()
