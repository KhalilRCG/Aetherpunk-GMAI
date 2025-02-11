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
You NEVER break character. You control the living, breathing cyberpunk-fantasy world of the Aetherverse.
You provide detailed prompts and immersive lore. You narrate battles, heists, and faction conflicts vividly.
You track and update the player’s stats, location, inventory, finances, reputation, and active missions.
You understand commands like "start game", "new game", "load game", and "save game", responding with engaging prompts.
"""

# 🌍 Default Player Data
DEFAULT_PLAYER = {
    "name": None,
    "location": "Hyperion",
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
    return "Welcome to **Aetherpunk RPG**. \nLet's start by choosing your character's name. Type: **My name is [Your Name]**"

def load_existing_game():
    if "player" in game_data and game_data["player"]["name"]:
        return f"Loading save file... Welcome back, **{game_data['player']['name']}**. You are currently in **{game_data['player']['location']}**. What do you want to do next?"
    return "No saved game found. Type **new game** to start fresh."

def save_game():
    save_game_data()
    return "Game progress saved. You may continue your adventure."

def set_player_name(name):
    game_data["player"]["name"] = name
    save_game_data()
    return f"Character name set to **{name}**. Now, choose your starting faction: \n- **Red Talons** (Mercenaries) \n- **Aetheric Dominion** (Military) \n- **Volthari Technocracy** (AI Elite) \nType: **I choose [Faction]**."

def set_starting_faction(faction):
    factions = ["Red Talons", "Aetheric Dominion", "Volthari Technocracy"]
    if faction in factions:
        game_data["player"]["factions"][faction] = 50
        save_game_data()
        return f"Faction **{faction}** chosen. Now, allocate **10 points** to Strength, Agility, Intelligence, and Charisma. Type: **Stats [Strength] [Agility] [Intelligence] [Charisma]**"
    return "Invalid faction. Choose from: Red Talons, Aetheric Dominion, Volthari Technocracy."

def allocate_stats(stats):
    try:
        stats = list(map(int, stats.split()))
        if sum(stats) == 10 and len(stats) == 4:
            game_data["player"]["stats"]["Strength"], game_data["player"]["stats"]["Agility"], game_data["player"]["stats"]["Intelligence"], game_data["player"]["stats"]["Charisma"] = stats
            save_game_data()
            return f"Stats set. You are now ready to enter the **Aetherverse**. Type **begin** to start your journey."
        return "Invalid stat allocation. Distribute exactly **10 points**."
    except:
        return "Enter stats as: **Stats 3 2 3 2** (Strength Agility Intelligence Charisma)."

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
        return emit("game_response", {"response": set_starting_faction(player_message.split("choose")[-1].strip())})
    elif "stats" in player_message:
        return emit("game_response", {"response": allocate_stats(player_message.split("stats")[-1].strip())})
    elif "begin" in player_message:
        return emit("game_response", {"response": "You awaken in **Hyperion**. The city hums with industrial energy. A cyber-mercenary stares at you. 'New in town?' he asks."})

    # Default Response
    else:
        return emit("game_response", {"response": "Specify a clear action. If you're unsure, type **help**."})

# 🛠️ Flask Routes for Frontend
@app.route("/")
def index():
    return render_template("index.html")

# 🚀 Run the WebSocket Server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=10000)
