import streamlit as st
import pandas as pd

st.set_page_config(page_title="CodeMotion - Robotics & Embedded Systems", layout="wide")

st.title("🤖 CodeMotion: Robotics and Embedded Engineering Intelligence")
st.caption("Firmware generation, ROS2 integration, and simulated behavior design with GPT-4.5")

# Sidebar
st.sidebar.title("CodeMotion Parameters")
hardware_target = st.sidebar.selectbox("Select Target Hardware", [
    "ESP32", "Raspberry Pi 4", "Arduino Mega", "STM32F4", "Jetson Nano"
])
ros_support = st.sidebar.radio("ROS2 Integration?", ["Yes", "No"])
selected_behavior = st.sidebar.selectbox("Behavior Type", [
    "Autonomous Navigation", "Pick and Place", "Line Following", "Gesture Response"
])

if st.sidebar.button("Generate Code & Behavior"):
    st.session_state["run_codemotion"] = True

# Tabbed Layout
tab1, tab2, tab3 = st.tabs(["🔧 Firmware", "📡 ROS2 Stack", "🎮 Behavior Simulator"])

with tab1:
    st.subheader("🔧 Generated Firmware (C/C++)")
    st.code("""
#include <Arduino.h>
void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT);
}
void loop() {
  digitalWrite(2, HIGH);
  delay(500);
  digitalWrite(2, LOW);
  delay(500);
}
    """, language="cpp")
    st.success("Firmware logic generated for selected behavior")

with tab2:
    st.subheader("📡 ROS2 Launch Stack")
    st.markdown("🔁 ROS2 launch file + topic tree")
    st.code("""
<launch>
  <node pkg="motion_control" type="nav_node" name="navigator" output="screen" />
  <node pkg="sensor_msgs" type="lidar_node" name="lidar" />
  <node pkg="cmd_vel_publisher" type="controller_node" name="motion_cmd" />
</launch>
    """, language="xml")
    st.success("ROS2 package scaffolding available")

with tab3:
    st.subheader("🎮 Simulated Behavior Plan")
    behavior_plan = {
        "Step": ["Start", "Scan Environment", "Detect Obstacle", "Path Re-plan", "Resume"],
        "Action": ["Boot sensors", "360° Lidar Sweep", "Classify shape", "Adjust path", "Continue"]
    }
    st.table(pd.DataFrame(behavior_plan))
    st.info("🧠 GPT-4.5 suggests including ultrasonic sensor for better proximity awareness")

st.markdown("---")
st.markdown("© 2025 Discover Software Solutions • CodeMotion Robotics Intelligence")
