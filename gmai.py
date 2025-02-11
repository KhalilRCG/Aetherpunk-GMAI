import random
import eventlet
import json
import os
import openai
import traceback
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Initialize Flask & WebSocket
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

# OpenAI API Key (Replace with your actual API key)
openai.api_key = "YOUR_OPENAI_API_KEY"

# 📁 Data Persistence: Load or Create Save File
SAVE_FILE = "game_data.json"

def load_data(file_name, default_value):
    """Loads JSON data from a file or returns a default value if the file doesn't exist."""
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return default_value

def save_data(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)

# Load game data
game_data = load_data(SAVE_FILE, {"player": None})

# 🌍 Default Player Data
DEFAULT_PLAYER = {
    "name": None,
    "species": None,
    "archetype": None,
    "planet": "Hyperion",
    "occupation": None,
    "origin_story": None,
    "location": "Hyperion - Lower District",
    "level": 1,
    "experience": 0,
    "credits": {"AetherCreds": 0, "AuroCreds": 500, "NeuroCreds": 200},
    "stats": {"HP": 100, "Strength": 5, "Agility": 5, "Intelligence": 5, "Charisma": 5},
    "inventory": [],
    "factions": {"Aetheric Dominion": -100, "Red Talons": 0, "Volthari Technocracy": 0},
    "bounty": 0,
    "business": None,
    "ship": {"status": "Standard", "shields": 100, "weapons": "Basic", "engines": "Standard"},
    "history": [],
    "last_prompt": None
}

# 🌟 AI-Powered Storytelling
def generate_dynamic_story(player_message):
    """Generates dynamic responses while referencing past interactions."""
    player_context = "\n".join(game_data["player"].get("history", []))  
    prompt = f"{player_context}\nPlayer: {player_message}\nGM:"
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    ).get("choices", [{}])[0].get("text", "").strip()
    
    game_data["player"]["history"].append(f"Player: {player_message}")
    game_data["player"]["history"].append(f"GM: {response}")
    save_data(SAVE_FILE, game_data)
    
    return response

# 🌟 Game Interaction Handling
@socketio.on("chat_message")
def handle_chat_message(data):
    player_message = data.get("message", "").strip()
    response = generate_dynamic_story(player_message)
    return emit("game_response", {"response": response})

# 🚀 Run the WebSocket Server
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's PORT env variable
    socketio.run(app, host="0.0.0.0", port=port)

