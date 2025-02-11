import os
import json
import random
import eventlet
import openai
import traceback 
from flask import Flask, send_from_directory, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Initialize Flask & WebSocket
app = Flask(__name__, static_folder="static")
CORS(app)
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

# OpenAI API Key (Replace with your actual API key)
openai.api_key = "YOUR_OPENAI_API_KEY"

# 📁 Load or Create Save File
SAVE_FILE = "game_data.json"

def load_data():
    """Loads JSON game data or initializes a new game session."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {"player": None}

def save_data():
    """Saves the game session persistently."""
    with open(SAVE_FILE, "w") as f:
        json.dump(game_data, f, indent=4)

# Load game data
game_data = load_data()

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

# 🌟 Abbreviation Matching
ABBREVIATIONS = {
    "merc": "Mercenary",
    "hack": "Hacker",
    "med": "Medic",
    "eng": "Engineer",
    "shop": "Open Shop",
    "buy": "Shopping Menu",
    "sell": "Sell Items"
}

def parse_input(user_input):
    """Matches abbreviations with full responses."""
    words = user_input.lower().split()
    for word in words:
        if word in ABBREVIATIONS:
            return ABBREVIATIONS[word]
    return user_input

# 🌟 AI-Powered Storytelling
def generate_dynamic_story(player_message):
    """Generates AI responses while remembering game history."""
    try:
        player_message = parse_input(player_message)
        player_context = "\n".join(game_data["player"].get("history", []))  
        prompt = f"{player_context}\nPlayer: {player_message}\nGM:"
        
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        ).get("choices", [{}])[0].get("text", "").strip()
        
        game_data["player"]["history"].append(f"Player: {player_message}")
        game_data["player"]["history"].append(f"GM: {response}")
        save_data()
        
        return response
    except Exception as e:
        return "⚠️ Error processing request. Try again later."

@socketio.on("chat_message")
def handle_chat_message(data):
    """Handles user messages and generates AI responses."""
    player_message = data.get("message", "").strip()
    if not game_data.get("player"):
        game_data["player"] = DEFAULT_PLAYER.copy()
    
    response = generate_dynamic_story(player_message)
    return emit("game_response", {"response": response})

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
