import requests
import os

API_BASE_URL = os.getenv("BACKEND_URL", "https://enginuity-backend.up.railway.app")

def post_prompt_to_agent(module: str, prompt: str, simulation_type: str = None):
    endpoint = f"{API_BASE_URL}/v1/{module}/analyze"
    try:
        payload = {"prompt": prompt}
        if simulation_type:
            payload["simulation_type"] = simulation_type
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
