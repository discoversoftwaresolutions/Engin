# app.py – Streamlit Entry Point
import streamlit as st
from modules.simulai import render_dashboard as simulai_ui
from modules.visuai import render_dashboard as visuai_ui
from modules.protoprint import render_dashboard as protoprint_ui
from modules.circuitiq import render_dashboard as circuitiq_ui
from modules.codemotion import render_dashboard as codemotion_ui
from modules.flowcore import render_dashboard as flowcore_ui
from modules.aeroiq import render_dashboard as aeroiq_ui
from modules.fusionx import render_dashboard as fusionx_ui

# Sidebar Navigation
st.sidebar.title("🔧 Enginuity Suite")
app_choice = st.sidebar.radio("Choose a module:", [
    "🧠 SimulAI", "🎨 VisuAI", "🛠️ ProtoPrint", "🔌 CircuitIQ",
    "📜 CodeMotion", "🌊 FlowCore", "✈️ AeroIQ", "🔬 FusionX"
])

# Route to appropriate module
if app_choice == "🧠 SimulAI":
    simulai_ui()
elif app_choice == "🎨 VisuAI":
    visuai_ui()
elif app_choice == "🛠️ ProtoPrint":
    protoprint_ui()
elif app_choice == "🔌 CircuitIQ":
    circuitiq_ui()
elif app_choice == "📜 CodeMotion":
    codemotion_ui()
elif app_choice == "🌊 FlowCore":
    flowcore_ui()
elif app_choice == "✈️ AeroIQ":
    aeroiq_ui()
elif app_choice == "🔬 FusionX":
    fusionx_ui()
