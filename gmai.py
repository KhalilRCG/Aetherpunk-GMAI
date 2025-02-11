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
LEARNING_FILE = "learning_data.json"

def load_data(file_name, default_value):
    """Loads JSON data from a file or returns a default value if the file doesn't exist."""
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return default_value

def save_data(file_name, data):
    """Saves JSON data to a file."""
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

# Load game and learning data
game_data = load_data(SAVE_FILE, {})
learning_data = load_data(LEARNING_FILE, {})

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
    "last_prompt": None,
    "pending_name": None
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

# 🌟 **Self-Learning System**
def learn_response(user_input, bot_response):
    """Stores player inputs and chatbot responses for future learning."""
    learning_data[user_input] = bot_response
    save_data(LEARNING_FILE, learning_data)

def get_learned_response(user_input):
    """Retrieves a response from the chatbot's memory if a similar input exists."""
    return learning_data.get(user_input, None)

# 📍 Character Creation & Game Setup
def start_new_game():
    game_data["player"] = DEFAULT_PLAYER.copy()
    save_data(SAVE_FILE, game_data)
    game_data["player"]["last_prompt"] = "confirm_new_game"
    return "🌌 **Start a new game? (yes/no)**"

def confirm_new_game(response):
    if response in ["yes", "y"]:
        game_data["player"] = DEFAULT_PLAYER.copy()
        save_data(SAVE_FILE, game_data)
        game_data["player"]["last_prompt"] = "name_prompt"
        return "🎭 **So what do we call you?** Type your name."
    return "❌ **Cancelled.** Returning to previous prompt."

def set_player_name(name):
    game_data["pending_name"] = name  # Store for confirmation
    game_data["player"]["last_prompt"] = "confirm_name"
    return f"🔷 **You chose `{name}`. Confirm? (yes/no)**"

def confirm_name(response):
    if response in ["yes", "y"]:
        game_data["player"]["name"] = game_data["pending_name"]
        save_data(SAVE_FILE, game_data)
        game_data["player"]["last_prompt"] = "species_prompt"
        return f"✅ **Got it, {game_data['player']['name']}**. Now pick your **species**: Aetherion, Pyronax, or Volthari."
    return "❌ **Name change cancelled.** What name should I call you?"

# 🚀 Game Interaction Handling
@socketio.on("chat_message")
def handle_chat_message(data):
    player_message = data.get("message", "").strip()

    # **Self-Learning Check**
    learned_response = get_learned_response(player_message)
    if learned_response:
        return emit("game_response", {"response": learned_response})

    # **Infer Meaning for "New Game" Inputs**
    if infer_player_intent(player_message) == "start_game":
        return emit("game_response", {"response": start_new_game()})

    # **Yes/No Confirmation Screens**
    if game_data["player"]["last_prompt"] == "confirm_new_game":
        return emit("game_response", {"response": confirm_new_game(player_message.lower())})

    if game_data["player"]["last_prompt"] == "confirm_name":
        return emit("game_response", {"response": confirm_name(player_message.lower())})

    # **Handling Name Input**
    if game_data["player"]["last_prompt"] == "name_prompt":
        return emit("game_response", {"response": set_player_name(player_message)})

    # **Learn from Mistakes (If the bot gets corrected)**
    if "wrong" in player_message or "not right" in player_message:
        game_data["player"]["last_prompt"] = "correct_response"
        return emit("game_response", {"response": "🤖 **Got it!** What should I have said instead?"})

    if game_data["player"]["last_prompt"] == "correct_response":
        learn_response(game_data["player"]["last_input"], player_message)
        game_data["player"]["last_prompt"] = None
        return emit("game_response", {"response": "✅ **Understood!** I'll remember that next time."})

    # **Unknown Input (Learn from the player)**
    game_data["player"]["last_input"] = player_message
    game_data["player"]["last_prompt"] = "correct_response"
    return emit("game_response", {"response": "🌀 **I’m not sure... how should I respond to that next time?**"})

# 🛠️ Flask Routes for Frontend
@app.route("/")
def index():
    return render_template("index.html")

# 🚀 Run the WebSocket Server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=10000)
