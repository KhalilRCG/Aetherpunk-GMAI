import random
import eventlet
import json
import os
import re
from flask import Flask, render_template
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

# 🌐 Intelligent Input Parsing
def extract_valid_choice(user_input, valid_choices):
    """Checks if the user's input contains a valid choice (even within a sentence)."""
    for choice in valid_choices:
        if re.search(rf"\b{choice}\b", user_input, re.IGNORECASE):
            return choice
    return None

# 📍 Character Creation & Game Setup
def start_new_game():
    global game_data  # Ensure full reset
    game_data["player"] = DEFAULT_PLAYER.copy()
    save_game_data()
    return "🌌 **Welcome to Aetherpunk RPG.**\nLet's start with your name. Say: `I'm [Name]` or `Call me [Name]`."

def set_player_name(name):
    game_data["player"]["name"] = name
    save_game_data()
    return f"✅ Got it, **{name}**. Now pick your **species**:\n\n- **Aetherion** (Hybrid beings, connected to Aetheric energy)\n- **Pyronax** (Plasma warriors, unbreakable)\n- **Volthari** (Cybernetic masterminds)\n\nType it however you want, I’ll understand."

def set_species(species):
    species = extract_valid_choice(species, ["Aetherion", "Pyronax", "Volthari"])
    if species:
        game_data["player"]["species"] = species
        save_game_data()
        return f"🔥 **{species}? Good call.** Now, pick an **archetype**:\n\n- **Hacker (Hack)** (Cyberwarfare expert)\n- **Mercenary (Merc)** (Elite combat specialist)\n- **Smuggler (Smug)** (Master of deception & trade)\n\nJust say the name or a short form, I’ll get it."
    return "❌ That species doesn't exist in the Aetherverse. Try again."

# 🚀 Game Interaction Handling
@socketio.on("chat_message")
def handle_chat_message(data):
    player_message = data.get("message", "").strip().lower()

    # Game Start Commands
    if "new game" in player_message or "start game" in player_message:
        game_data["player"] = DEFAULT_PLAYER.copy()
        save_game_data()
        return emit("game_response", {"response": start_new_game()})

    elif "help" in player_message:
        return emit("game_response", {"response": "🤖 **Help Menu:** Try saying `I'm [Name]` or `I want to be Pyronax`."})

    elif player_message.startswith(("i'm", "call me", "my name is", "name me")):
        name = player_message.split()[-1].title()
        return emit("game_response", {"response": set_player_name(name)})

    elif extract_valid_choice(player_message, ["Aetherion", "Pyronax", "Volthari"]):
        return emit("game_response", {"response": set_species(player_message)})

    else:
        return emit("game_response", {"response": "🌀 Huh? Sounds cryptic, but this is the Aetherverse. Let's roll with it. What's next?"})

# 🛠️ Flask Routes for Frontend
@app.route("/")
def index():
    return render_template("index.html")

# 🚀 Run the WebSocket Server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=10000)
