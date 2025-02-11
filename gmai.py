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
    "missions": [],
    "last_prompt": None
}

# 🌐 Context-Aware Input Recognition
def extract_valid_choice(user_input, valid_choices):
    """Checks if the user's input contains a valid choice (even within a sentence)."""
    for choice in valid_choices:
        if re.search(rf"\b{choice}\b", user_input, re.IGNORECASE):
            return choice
    return None

def infer_player_intent(user_input):
    """Dynamically interprets user intent from ANY valid Aetherpunk concept."""
    keywords = {
        "start_game": ["start", "new", "begin", "restart"],
        "shop": ["shop", "shopping", "store", "market", "vendor", "buy", "sell"],
        "weapons": ["weapons", "guns", "firearms", "blades", "armory"],
        "cyberware": ["cyberware", "implants", "augmentations", "mods", "upgrades"],
        "ships": ["ship", "starship", "spaceship", "freighter", "vessel"],
        "credits": ["credits", "money", "currency", "aethercreds", "aurocreds", "neurocreds"],
        "missions": ["mission", "job", "task", "quest", "bounty"],
        "travel": ["travel", "move", "relocate", "warp", "jump", "leave", "fly"],
        "go_back": ["back", "go back", "return", "previous"]
    }

    for category, words in keywords.items():
        if any(word in user_input for word in words):
            return category
    return None

# 📍 Character Creation & Game Setup
def start_new_game():
    game_data["player"] = DEFAULT_PLAYER.copy()
    save_game_data()
    game_data["player"]["last_prompt"] = "confirm_new_game"
    return "🌌 **Start a new game? (yes/no)**"

def confirm_new_game(response):
    if response in ["yes", "y"]:
        game_data["player"] = DEFAULT_PLAYER.copy()
        save_game_data()
        game_data["player"]["last_prompt"] = "name_prompt"
        return "🎭 **Let's start with your name.** Say: `I'm [Name]` or `Call me [Name]`."
    return "❌ **Cancelled.** Returning to previous prompt."

def confirm_action(response, action):
    if response in ["yes", "y"]:
        if action == "save":
            save_game_data()
            return "💾 **Game saved!** Back to business."
        elif action == "load":
            return load_existing_game()
    return "❌ **Cancelled.** Returning to previous prompt."

def load_existing_game():
    if "player" in game_data and game_data["player"]["name"]:
        return f"Loading save file... Welcome back, **{game_data['player']['name']}**. What’s next?"
    return "No saved game found. Type **new game** to start fresh."

def set_player_name(name):
    game_data["player"]["last_prompt"] = "confirm_name"
    return f"🔷 **You chose `{name}`. Confirm? (yes/no)**"

def confirm_name(response, name):
    if response in ["yes", "y"]:
        game_data["player"]["name"] = name
        save_game_data()
        game_data["player"]["last_prompt"] = "species_prompt"
        return f"✅ **Got it, {name}.** Now pick your **species**: Aetherion, Pyronax, or Volthari."
    return "❌ **Name change cancelled.** What name should I call you?"

# 🚀 Game Interaction Handling
@socketio.on("chat_message")
def handle_chat_message(data):
    player_message = data.get("message", "").strip().lower()

    # **Infer Meaning for "New Game" Inputs**
    if infer_player_intent(player_message) == "start_game":
        return emit("game_response", {"response": start_new_game()})

    # **Yes/No Confirmation Screens**
    if game_data["player"]["last_prompt"] == "confirm_new_game":
        return emit("game_response", {"response": confirm_new_game(player_message)})

    if game_data["player"]["last_prompt"] == "confirm_name":
        return emit("game_response", {"response": confirm_name(player_message, game_data['player']['name'])})

    # **Help Command Fix (Returns to Previous Prompt)**
    if "help" in player_message:
        return emit("game_response", {"response": "📜 **Tip:** Just type what you want! Example: `I want cyberware.`\n\nReturning to previous prompt..."})

    # **"Go Back" Command to Return to Last Prompt**
    if infer_player_intent(player_message) == "go_back":
        return emit("game_response", {"response": f"🔄 Returning to last prompt: {game_data['player']['last_prompt']}"})

    # **Dynamic Inferred Inputs for Shops, Missions, etc.**
    inferred_category = infer_player_intent(player_message)
    if inferred_category:
        responses = {
            "shop": "🛒 **You want to shop?** Here’s a vendor list: 1) Weapons, 2) Cyberware, 3) Ships, 4) Black Market Mods. What are you buying?",
            "weapons": "🔫 **Weapons Available:** Plasma Rifles (500 AC), Laser Blades (700 AC), Ion Shotguns (1200 AC). Interested?",
            "cyberware": "🤖 **Cyberware Upgrades:** Neural Hacks (1200 NC), Reflex Boosters (2500 NC), Stealth Cloaks (3000 NC). What do you want?",
            "missions": "📜 **Available Missions:** 1) Data Heist (8000 NC), 2) Merc Job (10K AC), 3) Smuggling Run (12K AC). Pick one."
        }
        return emit("game_response", {"response": responses[inferred_category]})

    return emit("game_response", {"response": "🌀 **Mysterious words... but this is the Aetherverse. Let's roll with it. What's next?**"})

# 🛠️ Flask Routes for Frontend
@app.route("/")
def index():
    return render_template("index.html")

# 🚀 Run the WebSocket Server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=10000)
