import streamlit as st
from pages.aeroiq import render_aeroiq_dashboard
from pages.flowcore import render_flowcore_dashboard
from pages.fusionx import render_fusionx_dashboard
from pages.simulai import render_simulai_dashboard
from pages.visuai import render_visuai_dashboard
from pages.protoprint import render_protoprint_dashboard
from pages.circuitiq import render_circuitiq_dashboard
from pages.codemotion import render_codemotion_dashboard

# Configure page
st.set_page_config(
    page_title="Enginuity Agentic Suite",
    layout="wide",
    page_icon="🧠"
)

# Sidebar Navigation
st.sidebar.title("🧠 Enginuity Suite")
app_selection = st.sidebar.radio(
    "Select Engineering Module",
    (
        "AeroIQ – Aerospace",
        "FlowCore – Digital Twin & Compliance",
        "FusionX – Energy & Plasma",
        "Simulai – Simulation AI",
        "VisuAI – Visual Intelligence",
        "ProtoPrint – Additive MFG",
        "CircuitIQ – Electronics",
        "CodeMotion – Robotics Code"
    )
)

# Route Logic
if app_selection == "AeroIQ – Aerospace":
    render_aeroiq_dashboard()

elif app_selection == "FlowCore – Digital Twin & Compliance":
    render_flowcore_dashboard()

elif app_selection == "FusionX – Energy & Plasma":
    render_fusionx_dashboard()

elif app_selection == "Simulai – Simulation AI":
    render_simulai_dashboard()

elif app_selection == "VisuAI – Visual Intelligence":
    render_visuai_dashboard()

elif app_selection == "ProtoPrint – Additive MFG":
    render_protoprint_dashboard()

elif app_selection == "CircuitIQ – Electronics":
    render_circuitiq_dashboard()

elif app_selection == "CodeMotion – Robotics Code":
    render_codemotion_dashboard()

else:
    st.warning("Unknown module selected. Please choose from the sidebar.")
