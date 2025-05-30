import asyncio
import websockets
import json

async def send_aeroiq_command(uri, payload):
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps(payload))
        response = await websocket.recv()
        return json.loads(response)

# Example usage:
# asyncio.run(send_aeroiq_command("ws://localhost:8000/ws/aeroiq", {"command": "start_sim"}))
