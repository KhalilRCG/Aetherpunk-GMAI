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
socketio = SocketIO(app, async_mode="eventlet")

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

# 🎭 Game Master AI (GMAI) Core Personality
GMAI_PERSONALITY = """
You are the Aetherpunk Game Master AI (GMAI).
You NEVER break character. You control the immersive cyberpunk-fantasy world of the Aetherverse.
You prompt the player for every major decision, guiding them through a fully interactive experience.
You generate events, activities, and opportunities relevant to the player's location.
You adapt dynamically, providing engaging story elements based on any user input.
"""

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
    "factions": {"Red Talons": 0, "Aetheric Dominion": -50, "Volthari Technocracy": 10},
    "missions": []
}

# 🎲 Skill Check Mechanic
def skill_check(stat, difficulty):
    roll = random.randint(1, 100)
    return (roll + game_data["player"]["stats"][stat]) >= difficulty, roll

# 📍 Character Creation & Game Setup
def start_new_game():
    game_data["player"] = DEFAULT_PLAYER.copy()
    save_game_data()
    return ("Welcome to **Aetherpunk RPG**. \nLet's begin by choosing your **character's name**."
            "\nType: **My name is [Your Name]**")

def load_existing_game():
    if "player" in game_data and game_data["player"]["name"]:
        return (f"Loading save file... Welcome back, **{game_data['player']['name']}**."
                f"\nYou are currently in **{game_data['player']['location']}**. What do you want to do next?")
    return "No saved game found. Type **new game** to start fresh."

def save_game():
    save_game_data()
    return "Game progress saved."

def set_player_name(name):
    game_data["player"]["name"] = name
    save_game_data()
    return ("Character name set. Now, choose your **species**:"
            "\n- **Aetherion** (Hybrid beings, connected to the Aetheric energy)"
            "\n- **Pyronax** (Plasma-based warriors, strong and durable)"
            "\n- **Volthari** (Electrokinetic cybernetic species)"
            "\nType: **I choose [Species]**")

def set_species(species):
    valid_species = ["Aetherion", "Pyronax", "Volthari"]
    if species in valid_species:
        game_data["player"]["species"] = species
        save_game_data()
        return ("Species set. Now, choose your **RPG archetype**:"
                "\n- **Hacker** (Master of cyberwarfare)"
                "\n- **Mercenary** (Combat expert, skilled in ranged/melee combat)"
                "\n- **Smuggler** (Underworld expert, fast-talker and trader)"
                "\nType: **I choose [Archetype]**")
    return "Invalid species. Choose: Aetherion, Pyronax, or Volthari."

def set_archetype(archetype):
    valid_archetypes = ["Hacker", "Mercenary", "Smuggler"]
    if archetype in valid_archetypes:
        game_data["player"]["archetype"] = archetype
        save_game_data()
        return ("Archetype set. Now, choose your **starting planet**:"
                "\n- **Hyperion** (Military-Industrial world, corporate power struggles)"
                "\n- **Helios** (Cyberpunk capital, dominated by AI and tech syndicates)"
                "\n- **Aethos** (Aetheric hybrid world, home to scientific anomalies)"
                "\nType: **I choose [Planet]**")
    return "Invalid archetype. Choose: Hacker, Mercenary, or Smuggler."

# 🚀 Game Interaction Handling
@socketio.on("chat_message")
def handle_chat_message(data):
    player_message = data.get("message", "").lower()

    # Game Start Commands
    if "new game" in player_message or "start game" in player_message:
        return emit("game_response", {"response": start_new_game()})
    elif "load game" in player_message:
        return emit("game_response", {"response": load_existing_game()})
    elif "save game" in player_message:
        return emit("game_response", {"response": save_game()})

    # Character Creation Commands
    elif "name is" in player_message:
        return emit("game_response", {"response": set_player_name(player_message.split("is")[-1].strip())})
    elif "choose" in player_message:
        words = player_message.split()
        if "species" in words:
            return emit("game_response", {"response": set_species(words[-1].capitalize())})
        elif "archetype" in words:
            return emit("game_response", {"response": set_archetype(words[-1].capitalize())})

    # Default Response
    else:
        return emit("game_response", {"response": "Specify a clear action. If unsure, type **help**."})

# 🛠️ Flask Routes for Frontend
@app.route("/")
def index():
    return render_template("index.html")

# 🚀 Run the WebSocket Server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=10000)
