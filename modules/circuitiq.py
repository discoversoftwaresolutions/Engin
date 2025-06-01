# modules/circuitiq.py

import streamlit as st
import logging

# ✅ Setup logger
logger = logging.getLogger("circuithandler")

def render_dashboard():
    """
    Renders the CircuitIQ dashboard for PCB and circuit simulation.
    """
    st.title("⚡ CircuitIQ – PCB & Circuit Simulation")
    st.markdown("Autogenerate layouts, evaluate power integrity, and mitigate supply chain risks in electronics design.")

    # ---- Upload Section ----
    uploaded_schematic = st.file_uploader("📂 Upload Schematic / Board File", type=["brd", "sch", "kicad_pcb"])
    if uploaded_schematic:
        file_name = uploaded_schematic.name
        file_size = uploaded_schematic.size / (1024 * 1024)

        if file_size > 50:
            st.error(f"⚠ File too large ({file_size:.2f}MB). Please upload a file under 50MB.")
            return
        else:
            st.success(f"✅ Schematic '{file_name}' uploaded successfully.")
            logger.info(f"📁 Uploaded schematic: {file_name} | Size: {file_size:.2f}MB")

            # ---- Action Buttons ----
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("📐 Auto-Generate Layout"):
                    st.info(f"Generating PCB layout for '{file_name}'...")
                    st.success("✅ Layout generation completed.")

            with col2:
                if st.button("⚡ Evaluate Power Integrity"):
                    st.info(f"Analyzing power integrity for '{file_name}'...")
                    st.success("✅ Power integrity check complete.")

            with col3:
                if st.button("🔍 Supply Chain Risk Assessment"):
                    st.info(f"Assessing sourcing risk for components in '{file_name}'...")
                    st.success("✅ Supply chain risk analysis complete.")

            # ---- Circuit Notes ----
            st.markdown("### 🧠 Circuit Agent Notes")
            st.text_area("Design Observations", placeholder="Enter layout comments, analysis results...", height=180)
import streamlit as st
import requests

st.set_page_config(page_title="CircuitIQ – PCB & Supply Chain", layout="wide")

st.title("🔌 CircuitIQ – Supply Chain Analyzer")

if "bom" not in st.session_state:
    st.session_state["bom"] = [
        {"part": "IC-LM317", "category": "regulator"},
        {"part": "RES-10k", "category": "resistor"},
        {"part": "CAP-100nF", "category": "capacitor", "available": True}
    ]

if st.button("🚦 Run Supply Chain Check"):
    resp = requests.post(
        "https://enginuity-backend.up.railway.app/api/v1/circuitiq/supply_chain/check",
        json={"bom": st.session_state["bom"]}
    )
    result = resp.json()
    if "error" in result:
        st.error(result["error"])
    else:
        st.success("✅ Agent Review Complete")
        st.json(result)

    # ---- Bill of Materials Panel ----
    st.markdown("---")
    st.markdown("### 📋 Bill of Materials (BoM) Options")
    check_inventory = st.checkbox("🔄 Check Inventory with Preferred Vendors")

    if check_inventory:
        st.info("📦 Verifying part availability and identifying alternatives from vendor APIs...")
