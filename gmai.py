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
    return {
        "player": {
            "name": "Unknown",
            "location": "Hyperion",
            "credits": {"AetherCreds": 0, "AuroCreds": 500, "NeuroCreds": 200},
            "stats": {"Strength": 5, "Agility": 5, "Intelligence": 5, "Charisma": 5},
            "inventory": [],
            "factions": {"Red Talons": 0, "Aetheric Dominion": -50, "Volthari Technocracy": 10}
        }
    }

def save_game_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f, indent=4)

game_data = load_game_data()

# 🎭 Game Master AI (GMAI) Core Personality
GMAI_PERSONALITY = """
You are the Aetherpunk Game Master AI (GMAI). 
You NEVER break character. You control the living, breathing cyberpunk-fantasy world of the Aetherverse.
You dynamically track and update the player's progress, inventory, location, reputation, and finances.
You guide the player through full character creation, skill checks, turn-based combat, hacking, trading, smuggling, diplomacy, and war.
You process all inputs dynamically, ensuring a meaningful response for every interaction.
"""

# 🎲 Skill Check Mechanic
def skill_check(stat, difficulty):
    roll = random.randint(1, 100)
    return (roll + game_data["player"]["stats"][stat]) >= difficulty, roll

# 📍 Character Creation
def start_character_creation():
    return (
        "Welcome to **Aetherpunk RPG**.\n"
        "Let's create your character. Choose your name:"
    )

def set_player_name(name):
    game_data["player"]["name"] = name
    save_game_data(game_data)
    return f"Character name set to **{name}**. Now, choose your starting faction:\n" \
           "- Red Talons\n- Aetheric Dominion\n- Volthari Technocracy"

def set_starting_faction(faction):
    if faction.lower() in ["red talons", "aetheric dominion", "volthari technocracy"]:
        game_data["player"]["factions"][faction] = 50
        save_game_data(game_data)
        return f"Faction **{faction}** chosen. Now, allocate **10 points** to Strength, Agility, Intelligence, and Charisma."
    return "Invalid faction. Choose from: Red Talons, Aetheric Dominion, Volthari Technocracy."

def allocate_stats(stats):
    try:
        stats = list(map(int, stats.split()))
        if sum(stats) == 10 and len(stats) == 4:
            game_data["player"]["stats"]["Strength"], \
            game_data["player"]["stats"]["Agility"], \
            game_data["player"]["stats"]["Intelligence"], \
            game_data["player"]["stats"]["Charisma"] = stats
            save_game_data(game_data)
            return f"Stats set. You are now ready to enter the Aetherverse. Type 'begin' to start."
        return "Invalid stat allocation. Distribute exactly **10 points** across 4 stats."
    except:
        return "Enter stats in format: '3 2 3 2' (Strength Agility Intelligence Charisma)."

# ⚔️ Combat System
def handle_combat(enemy):
    success, roll = skill_check("Strength", 60)
    if success:
        return f"✅ You defeat **{enemy}**! (Roll: {roll})"
    else:
        return f"❌ You were injured fighting **{enemy}**. (Roll: {roll})"

# 💻 Hacking System
def handle_hacking(target):
    success, roll = skill_check("Intelligence", 65)
    if success:
        return f"✅ You successfully hack **{target}** and retrieve valuable data! (Roll: {roll})"
    else:
        return f"❌ Your hacking attempt on **{target}** failed. Security is alert! (Roll: {roll})"

# 🎭 AI-Driven Game Master Response Generator
@socketio.on("chat_message")
def handle_chat_message(data):
    player_message = data.get("message", "").lower()

    if "name is" in player_message:
        return emit("game_response", {"response": set_player_name(player_message.split("is")[-1].strip())})
    elif "faction" in player_message:
        return emit("game_response", {"response": set_starting_faction(player_message.strip())})
    elif "stats" in player_message:
        return emit("game_response", {"response": allocate_stats(player_message.split("stats")[-1].strip())})
    elif "begin" in player_message:
        return emit("game_response", {"response": "Welcome to Aetherpunk. Your journey begins in **Hyperion**."})
    elif "attack" in player_message:
        return emit("game_response", {"response": handle_combat("Cyber-Warrior Elite")})
    elif "hack" in player_message:
        return emit("game_response", {"response": handle_hacking("Volthari Data Vault")})
    else:
        return emit("game_response", {"response": "Specify a clear action."})

# 🛠️ Flask Routes for Frontend
@app.route("/")
def index():
    return render_template("index.html")

# 🚀 Run the WebSocket Server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=10000)
