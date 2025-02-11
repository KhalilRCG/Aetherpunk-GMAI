import random
import eventlet
import json
import os
import re
import traceback
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
ERROR_LOG = "error_log.txt"

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

# 🌟 AI Self-Learning System
def learn_response(user_input, bot_response):
    """Stores player inputs and chatbot responses for future learning."""
    learning_data[user_input] = bot_response
    save_data(LEARNING_FILE, learning_data)

def get_learned_response(user_input):
    """Retrieves a response from the chatbot's memory if a similar input exists."""
    return learning_data.get(user_input, None)

# 🚨 AI Self-Troubleshooting
def log_error(error_message):
    """Logs errors for troubleshooting and self-analysis."""
    with open(ERROR_LOG, "a") as f:
        f.write(f"{error_message}\n")

def self_diagnose():
    """Runs an internal diagnostic to identify any issues."""
    try:
        load_data(SAVE_FILE, {})
        load_data(LEARNING_FILE, {})
        return "✅ Self-diagnostic complete. No errors detected."
    except Exception as e:
        log_error(traceback.format_exc())
        return f"⚠️ **Error detected:** {str(e)}. Check `error_log.txt` for details."

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

# 🚀 Game Interaction Handling
@socketio.on("chat_message")
def handle_chat_message(data):
    player_message = data.get("message", "").strip()

    # **Self-Learning Check**
    learned_response = get_learned_response(player_message)
    if learned_response:
        return emit("game_response", {"response": learned_response})

    # **Self-Troubleshooting**
    if "diagnose" in player_message or "self-check" in player_message:
        return emit("game_response", {"response": self_diagnose()})

    # **Infer Meaning for "New Game" Inputs**
    if "start" in player_message or "new game" in player_message:
        return emit("game_response", {"response": start_new_game()})

    # **Handling Name Input**
    if game_data["player"]["last_prompt"] == "name_prompt":
        game_data["player"]["pending_name"] = player_message
        game_data["player"]["last_prompt"] = "confirm_name"
        return emit("game_response", {"response": f"🔷 **You chose `{player_message}`. Confirm? (yes/no)**"})

    return emit("game_response", {"response": "🌀 **I'm not sure... how should I respond to that next time?**"})

# 🛠️ Flask Routes for Frontend
@app.route("/")
def index():
    return render_template("index.html")

# 🚀 Run the WebSocket Server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=10000)
