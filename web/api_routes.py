import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from quest_manager import connect_websocket, active_connections

router = APIRouter()

@router.websocket("/ws/quests")
async def quest_websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections for real-time quest updates."""
    await websocket.accept()
    await connect_websocket(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get("action") == "ping":
                await websocket.send_text(json.dumps({"response": "pong"}))
    except WebSocketDisconnect:
        active_connections.remove(websocket)
