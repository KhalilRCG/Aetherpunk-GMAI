from backend.game_state import GameState
from backend.game_master_ai import GameMasterAI
from backend.economy import Economy
from backend.quest_engine import QuestEngine
from backend.factions import Factions
from backend.npc_ai import NPC_AI
from backend.city_builder import CityBuilder
from backend.heist_generator import HeistGenerator
from backend.black_market import BlackMarket


app = FastAPI()
game_state = GameState()
gm_ai = GameMasterAI()
economy = Economy()
npc_ai = NPC_AI()
quest_engine = QuestEngine()
city_builder = CityBuilder()
factions = Factions()
heist_generator = HeistGenerator()
black_market = BlackMarket()

active_connections = {}

@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    """Handles real-time multiplayer interactions."""
    await websocket.accept()
    active_connections[player_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            response = gm_ai.generate_event(data, game_state.load_state(player_id))
            await websocket.send_text(response)
    except WebSocketDisconnect:
        del active_connections[player_id]

@app.get("/start/{player_id}")
def start_game(player_id: str):
    """Initialize a new player session."""
    game_state.save_state(player_id, {"location": "Hyperion", "credits": {"AuroCreds": 1000}, "reputation": 0})
    return {"message": "Game started!", "player_state": game_state.load_state(player_id)}

@app.post("/quest/{player_id}")
def generate_quest(player_id: str):
    """Generate a dynamic quest for the player."""
    return {"quest": quest_engine.generate_quest(player_id)}

@app.post("/city/build/{player_id}")
def build_city(player_id: str):
    """Generate a new cyberpunk city based on player influence."""
    return {"city": city_builder.generate_city(player_id)}

@app.post("/factions/war/{faction1}/{faction2}")
def start_war(faction1: str, faction2: str):
    """Trigger war between two factions."""
    return factions.start_war(faction1, faction2)

@app.post("/heist/generate/{player_id}")
def generate_heist(player_id: str):
    """Generate a procedural heist mission."""
    return {"heist": heist_generator.generate_heist(player_id)}

@app.post("/black-market/trade/{item}/{amount}")
def trade_black_market(item: str, amount: int):
    """Trade black-market goods and services."""
    return {"value": black_market.trade(item, amount)}
