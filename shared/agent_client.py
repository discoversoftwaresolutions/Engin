import requests
import os
import logging
import json
import asyncio
import websockets

logger = logging.getLogger("agent-client")

API_BASE_URL = os.getenv("BACKEND_URL", "https://enginuity-backend.up.railway.app")
WS_BASE_URL = API_BASE_URL.replace("https://", "wss://").replace("http://", "ws://")


# === REST API ===
def post_prompt_to_agent(module: str, prompt: str, simulation_type: str = None, action: str = "analyze") -> dict:
    endpoint = f"{API_BASE_URL}/v1/{module}/{action}"
    payload = {"prompt": prompt}
    if simulation_type:
        payload["simulation_type"] = simulation_type

    try:
        logger.info(f"➡️ POST to {endpoint} | Payload: {payload}")
        response = requests.post(endpoint, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        logger.error(f"❌ HTTP error from {endpoint}: {http_err}")
        return {"error": f"HTTP {response.status_code}: {response.text}"}
    except Exception as e:
        logger.exception("❌ Unexpected error during agent call")
        return {"error": str(e)}


# === Agent Ping (used for home page status) ===
def ping_agent(module: str) -> bool:
    try:
        health_url = f"{API_BASE_URL}/v1/{module}/healthz"
        response = requests.get(health_url, timeout=2)
        return response.status_code == 200
    except Exception as e:
        logger.warning(f"Agent {module} unreachable: {e}")
        return False


# === WebSocket Streaming Support ===
async def stream_agent_response(module: str, payload: dict, endpoint: str = "stream"):
    """
    Async generator that yields streamed tokens/messages from agent WebSocket.

    Args:
        module (str): Module slug
        payload (dict): Command to send
        endpoint (str): WebSocket subroute, defaults to `/stream`

    Yields:
        str: Streamed chunks or tokens
    """
    ws_uri = f"{WS_BASE_URL}/ws/{module}/{endpoint}"
    try:
        async with websockets.connect(ws_uri) as websocket:
            await websocket.send(json.dumps(payload))
            async for message in websocket:
                yield message
    except Exception as e:
        logger.error(f"❌ WebSocket error with {ws_uri}: {e}")
        yield json.dumps({"error": str(e)})
