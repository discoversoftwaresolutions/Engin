import streamlit as st
import logging
import requests
from typing import Dict, Any
from datetime import datetime


# ✅ Setup Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("flowcore")

API_BASE_URL = "https://enginuity-production.up.railway.app/flowcore"  # ✅ Integrated production endpoint

def render_dashboard():
    """Renders the FlowCore - Digital Twin & Compliance dashboard."""

    st.title("🔄 FlowCore – Digital Twin & Compliance")
    st.markdown("**Sync, validate, and observe engineering systems with real-time digital twins and compliance logic.**")

    # ---- Sidebar Navigation ----
    st.sidebar.subheader("🧭 Select FlowCore Task")
    task_options = {
        "Sync Digital Twin State": "Synchronize the digital twin with real-world telemetry data.",
        "Track Engineering Changes": "Audit and version control your model state transitions.",
        "Validate Compliance Rules": "Run your twin against real-time or simulated compliance constraints."
    }

    task = st.sidebar.selectbox("Task Options", list(task_options.keys()))
    st.sidebar.markdown(f"ℹ **Description:** {task_options[task]}")

    # ---- User Input ----
    st.subheader(f"📌 Selected Task: {task}")
    prompt = st.text_area(
        "📄 Describe the system state or objective:",
        placeholder="e.g., Sync propulsion twin with telemetry snapshot from 2025-05-01T00:00Z..."
    )

    # ---- Task Execution ----
    if st.button("🚀 Execute Task"):
        if not prompt.strip():
            st.warning("⚠️ Please provide a detailed objective.")
            return

        timestamp = datetime.utcnow().isoformat()
        logger.info(f"[FlowCore] Task: {task} | Prompt: {prompt} | Timestamp: {timestamp}")

        try:
            res = requests.post(
                f"{API_BASE_URL}/execute-task",
                json={"task": task, "description": prompt, "timestamp": timestamp},
                timeout=10
            )
            if res.status_code == 200:
                response_data = res.json()
                st.success("✅ Task Completed")
                st.json(response_data)
                logger.info("✅ FlowCore task executed successfully.")
            else:
                st.error(f"⚠️ API Error: {res.text}")
                logger.error(f"❌ FlowCore API error: {res.status_code} - {res.text}")
        except Exception as e:
            st.error(f"⚠️ Failed to execute task: {e}")
            logger.error(f"❌ API request failed: {e}")

    # ---- Footer ----
    st.markdown("---")
    st.markdown("FlowCore – A Discover Software Solutions Module • 2025")

if __name__ == "__main__":
    render_dashboard()
