import asyncio
import websockets
import json
import logging

API_BASE_URL = "https://enginuity-production.up.railway.app/aeroiq" 

# ✅ Setup logger
logger = logging.getLogger("aeroiq_ws")
logging.basicConfig(level=logging.INFO)

async def send_aeroiq_command(uri: str, payload: dict, timeout: int = 10) -> dict:
    """
    Sends a JSON command to an AeroIQ WebSocket endpoint and receives the response.

    Args:
        uri (str): WebSocket URI (e.g., ws://localhost:8000/ws/aeroiq)
        payload (dict): Command payload to send
        timeout (int): Timeout in seconds for the response

    Returns:
        dict: Decoded response from the server

    Raises:
        Exception: For connection or message-level failures
    """
    try:
        logger.info(f"🔗 Connecting to WebSocket: {uri}")
        async with websockets.connect(uri) as websocket:
            logger.info(f"📤 Sending payload: {payload}")
            await websocket.send(json.dumps(payload))

            response = await asyncio.wait_for(websocket.recv(), timeout=timeout)
            logger.info(f"📥 Received response: {response}")
            return json.loads(response)

    except asyncio.TimeoutError:
        logger.error("⏱ Timeout waiting for WebSocket response.")
        return {"error": "Timeout while waiting for server response"}

    except websockets.ConnectionClosedError as e:
        logger.error(f"🔌 WebSocket connection closed unexpectedly: {e}")
        return {"error": "WebSocket connection closed unexpectedly"}

    except Exception as e:
        logger.exception(f"❌ Unexpected error during WebSocket communication: {e}")
        return {"error": str(e)}

# ✅ Example usage
# if __name__ == "__main__":
#     result = asyncio.run(send_aeroiq_command("ws://localhost:8000/ws/aeroiq", {"command": "start_sim"}))
#     print(result)
