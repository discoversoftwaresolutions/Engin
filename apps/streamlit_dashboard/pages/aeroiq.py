import streamlit as st
import requests

st.set_page_config(page_title="AeroIQ - Aerospace Engineering", layout="wide")

st.title("🚀 AeroIQ - Aerospace Engineering Module")
st.markdown("Model-based systems engineering, propulsion, avionics, and orbital simulation powered by GPT-4.5 and quantum-enhanced algorithms.")

# Sidebar - Module selector
task = st.sidebar.selectbox("Select Task", [
    "CFD Solver",
    "Propulsion Optimizer",
    "Structural Analysis",
    "Orbital Prediction",
    "System Integration",
    "Quantum Payload Optimization",
    "Firmware Build",
    "Regulatory Compliance"
])

# Inputs
st.subheader(f"🛠️ Task: {task}")
prompt = st.text_area("Describe your objective", placeholder="E.g., Optimize nozzle design for supersonic cruise...")
uploaded_file = st.file_uploader("Upload Design/Data File", type=["json", "csv", "stl", "txt"])

# Run
if st.button("Run Task"):
    files = {"file": uploaded_file.getvalue()} if uploaded_file else None
    payload = {"task": task, "prompt": prompt}
    response = requests.post("http://localhost:8000/api/v1/aeroiq/run", data=payload, files=files)

    if response.status_code == 200:
        st.success("✅ Task Completed")
        st.json(response.json())
    else:
        st.error(f"❌ Error: {response.text}")
