from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect, Depends
from utils.database_handler import DatabaseHandler
from utils.logging_system import LoggingSystem

router = APIRouter()
db = DatabaseHandler()
logger = LoggingSystem()

@router.websocket("/ws/quests")
async def quest_websocket_endpoint(websocket: WebSocket):
    """Handles WebSocket connections for real-time quest updates."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Received: {data}")
    except WebSocketDisconnect:
        logger.log_event("WebSocket connection closed.")

@router.get("/api/factions")
def get_factions():
    """Retrieves all faction data from the database."""
    try:
        db.cursor.execute("SELECT * FROM factions")
        factions = db.cursor.fetchall()
        return {"factions": factions}
    except Exception as e:
        logger.log_error(f"Error retrieving factions: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/api/factions/update")
def update_faction(name: str, influence: int):
    """Updates faction influence dynamically."""
    try:
        db.update_faction_influence(name, influence)
        logger.log_event(f"Faction {name} influence updated by {influence}.")
        return {"message": f"Updated {name}'s influence."}
    except Exception as e:
        logger.log_error(f"Error updating faction influence: {e}")
        raise HTTPException(status_code=500, detail="Failed to update faction influence.")

@router.get("/api/players/{player_name}")
def get_player_data(player_name: str):
    """Fetches player details based on the player's name."""
    try:
        db.cursor.execute("SELECT * FROM players WHERE name = ?", (player_name,))
        player = db.cursor.fetchone()
        if not player:
            raise HTTPException(status_code=404, detail="Player not found")
        return {"player": player}
    except Exception as e:
        logger.log_error(f"Error retrieving player {player_name}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
