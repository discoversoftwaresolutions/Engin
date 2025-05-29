import streamlit as st

st.title("CodeMotion - Robotics & Embedded Systems")
st.write("Generate firmware, compose ROS2 behavior, and simulate robotics systems.")

firmware_target = st.selectbox("Target Platform", ["ESP32", "STM32", "Arduino", "Raspberry Pi"])
uploaded_code = st.file_uploader("Upload Hardware Specs / Code Snippet", type=["yaml", "json", "ino", "c", "cpp"])

if uploaded_code:
    st.success(f"Configuration '{uploaded_code.name}' loaded.")
    st.button("Generate Firmware")
    st.button("Compose ROS2 Behavior Tree")
    st.button("Run Behavior Simulation")

st.text_area("Code Agent Reasoning", height=200)
