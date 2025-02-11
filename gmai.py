import random
import eventlet
import json
import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Initialize Flask & WebSocket
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

# 📁 Data Persistence: Load or Create Save File
SAVE_FILE = "game_data.json"

def load_game_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_game_data():
    with open(SAVE_FILE, "w") as f:
        json.dump(game_data, f, indent=4)

game_data = load_game_data()

# 🌍 Default Player Data
DEFAULT_PLAYER = {
    "name": None,
    "species": None,
    "archetype": None,
    "planet": None,
    "occupation": None,
    "origin_story": None,
    "location": None,
    "credits": {"AetherCreds": 0, "AuroCreds": 500, "NeuroCreds": 200},
    "stats": {"Strength": 5, "Agility": 5, "Intelligence": 5, "Charisma": 5},
    "inventory": [],
    "factions": {"Aetheric Dominion": -100, "Red Talons": 0, "Volthari Technocracy": 0},
    "missions": []
}

# 🎲 Skill Check Mechanic
def skill_check(stat, difficulty):
    roll = random.randint(1, 100)
    return (roll + game_data["player"]["stats"][stat]) >= difficulty, roll

# 📍 Character Creation & Game Setup
def start_new_game():
    global game_data  # Ensure we reset game data correctly
    game_data["player"] = DEFAULT_PLAYER.copy()
    save_game_data()
    return ("🌌 Welcome to **Aetherpunk RPG**.\n\nLet's begin by choosing your **character's name**."
            "\nType: **My name is [Your Name]**")

def load_existing_game():
    if "player" in game_data and game_data["player"]["name"]:
        return (f"Loading save file... Welcome back, **{game_data['player']['name']}**."
                f"\nYou are currently in **{game_data['player']['location']}**. What do you want to do next?")
    return "No saved game found. Type **new game** to start fresh."

def save_game():
    save_game_data()
    return "💾 Game progress saved."

def set_player_name(name):
    game_data["player"]["name"] = name
    save_game_data()
    return ("✅ Character name set. Now, choose your **species**:"
            "\n- **Aetherion** (Hybrid beings, connected to Aetheric energy)"
            "\n- **Pyronax** (Plasma-based warriors, strong and durable)"
            "\n- **Volthari** (Electrokinetic cybernetic species)"
            "\nType your species choice.")

# 🚀 Game Interaction Handling
@socketio.on("chat_message")
def handle_chat_message(data):
    player_message = data.get("message", "").strip().lower()

    # Game Start Commands
    if "new game" in player_message or "start game" in player_message:
        emit("game_response", {"response": "🔄 Resetting game... please wait."}, broadcast=True)
        eventlet.sleep(1)  # Short delay to let the UI update
        return emit("game_response", {"response": start_new_game()}, broadcast=True)
    
    elif "load game" in player_message:
        return emit("game_response", {"response": load_existing_game()})
    
    elif "save game" in player_message:
        return emit("game_response", {"response": save_game()})

    elif player_message.startswith("my name is"):
        name = player_message.replace("my name is", "").strip().title()
        return emit("game_response", {"response": set_player_name(name)})

    # Default Response
    else:
        return emit("game_response", {"response": "🌀 I didn't quite get that, but let's keep moving forward! What do you want to do next?"})

# 🛠️ Flask Routes for Frontend
@app.route("/")
def index():
    return render_template("index.html")

# 🚀 Run the WebSocket Server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=10000)
