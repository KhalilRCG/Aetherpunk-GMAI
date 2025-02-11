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
openai.api_key = "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"

# 📁 Load or Create Save File
SAVE_FILE = "game_data.json"

def load_data():
    """Loads JSON game data or initializes a new game session."""
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {"player": None, "cities": {}, "factions": {}, "lore": {}}

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
    "location": "Lower District",
    "level": 1,
    "experience": 0,
    "credits": {"AetherCreds": 0, "AuroCreds": 500, "NeuroCreds": 200},
    "stats": {"HP": 100, "Strength": 5, "Agility": 5, "Intelligence": 5, "Charisma": 5},
    "inventory": ["Basic Blaster", "Medkit"],
    "factions": {"Aetheric Dominion": -100, "Red Talons": 0, "Volthari Technocracy": 0},
    "bounty": 0,
    "history": [],
    "last_prompt": None
}

# 🌟 Expanded Aetherverse Locations
PLANETS = {
    "Hyperion": ["Lower District", "Aurovium Mines", "Red Talon HQ"],
    "Helios": ["Neon Vortex", "Volthari High Court", "Cyber District"],
    "Aethos": ["Valkyron Prime", "Vaedropolis Prime", "Aetheric Spires"],
    "Outer Sectors": ["Uncharted Void", "Derelict Stations", "Pirate Strongholds"]
}

# 🌟 Expanded Factions
FACTIONS = {
    "Aetheric Dominion": "The supreme rulers of the Aetherverse, enforcing absolute control.",
    "Red Talons": "Hyperion's ruthless gang controlling Aurovium smuggling.",
    "Volthari Technocracy": "A council of cybernetic aristocrats ruling Helios.",
    "Null Cartel": "A network of AI smugglers and data traders in the void.",
    "Eclipse Syndicate": "A rogue mercenary group operating outside Dominion law."
}

# 🌟 Dynamic Lore Generation
def generate_lore(subject):
    """Creates new lore dynamically if it doesn't exist."""
    if subject in game_data["lore"]:
        return f"📜 {subject}: {game_data['lore'][subject]}"
    
    prompt = f"Generate deep lore about {subject} in the Aetherverse."
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=200
    ).get("choices", [{}])[0].get("text", "").strip()

    game_data["lore"][subject] = response
    save_data()
    return f"📖 Newly Discovered Lore: {response}"

# 🌟 Expanded AI Memory (Long-Term Context)
def generate_dynamic_story(player_message):
    """Generates AI responses while remembering extended game history."""
    try:
        game_data["player"]["history"] = game_data["player"]["history"][-30:]  # Keeps memory to 30 interactions

        prompt = f"{game_data['player']['history']}\nPlayer: {player_message}\nGM:"

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are the Aetherpunk Game Master, guiding the player through an interactive RPG adventure."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        ).get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        game_data["player"]["history"].append(f"Player: {player_message}")
        game_data["player"]["history"].append(f"GM: {response}")
        save_data()

        return response
    except Exception:
        return "⚠️ Error processing request. Try again later."



        game_data["player"]["history"].append(f"Player: {player_message}")
        game_data["player"]["history"].append(f"GM: {response}")
        save_data()

        return response
    except Exception:
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
