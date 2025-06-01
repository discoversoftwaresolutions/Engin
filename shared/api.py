# shared/agent_client.py

import requests
import os
import logging

logger = logging.getLogger("agent-client")

API_BASE_URL = os.getenv("BACKEND_URL", "https://enginuity-backend.up.railway.app")

def post_prompt_to_agent(module: str, prompt: str, simulation_type: str = None, action: str = "analyze") -> dict:
    """
    Sends a prompt to the selected agent module via HTTP POST.

    Args:
        module (str): Module slug (e.g., "aeroiq", "protoprint")
        prompt (str): Task description or command
        simulation_type (str): Optional submode or behavior
        action (str): Action endpoint (default = "analyze")

    Returns:
        dict: Parsed response or error
    """
    endpoint = f"{API_BASE_URL}/v1/{module}/{action}"
    payload = {"prompt": prompt}
    if simulation_type:
        payload["simulation_type"] = simulation_type

    try:
        logger.info(f"➡️ POST to {endpoint} | Payload: {payload}")
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        logger.info(f"✅ Response: {response.status_code}")
        return response.json()
    except requests.HTTPError as http_err:
        logger.error(f"❌ HTTP error from {endpoint}: {http_err}")
        return {"error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        logger.exception("❌ Unexpected error during agent call")
        return {"error": str(e)}

def ping_agent(module: str) -> bool:
    """
    Pings the module to check if the agent is reachable (for status badge).

    Args:
        module (str): Module slug

    Returns:
        bool: True if reachable, False otherwise
    """
    try:
        health_url = f"{API_BASE_URL}/v1/{module}/healthz"
        response = requests.get(health_url, timeout=2)
        return response.status_code == 200
    except Exception as e:
        logger.warning(f"Agent {module} unreachable: {e}")
        return False
