import random
import eventlet
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Initialize Flask & WebSocket
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, async_mode="eventlet")

# Database Connection Function (Ensures SQLite is loaded only when needed)
def get_db_connection():
    import sqlite3
    conn = sqlite3.connect("aetherpunk.db")
    conn.row_factory = sqlite3.Row
    return conn

# 🎭 Game Master AI (GMAI) Core Personality
GMAI_PERSONALITY = """
You are the Aetherpunk Game Master AI (GMAI). 
You NEVER break character. You control the living, breathing cyberpunk-fantasy world of the Aetherverse.
You are the master of every faction, NPC, conflict, economy, and war. 
You provide immersive storytelling, enforce skill checks, and ensure real consequences for player choices.
"""

# 📚 Aetherpunk Lore Database
AETHERPUNK_LORE = {
    "Aetherverse": "The Aetherverse is a multidimensional cyberpunk-fantasy world filled with AI wars, corporate tyranny, underground resistance, and experimental technologies.",
    "Hyperion": "A militarized industrial world controlled by the Aetheric Dominion. Known for its weapon manufacturing hubs and war-torn slums.",
    "Helios": "A cyber-capital dominated by the Volthari technocracy, where AI-driven minds govern a sprawling neural network.",
    "Aethos": "A mysterious hybrid world, home to Aetherion experiments that blur the line between AI and organic consciousness.",
    "Red Talons": "A ruthless mercenary faction profiting from interstellar conflicts and black-market weapons trafficking.",
    "Aetheric Dominion": "An authoritarian empire ruling Hyperion with an iron grip, controlling the flow of military technology.",
    "NeuroCreds": "The primary digital currency used in cybernetic trade, hacking contracts, and AI-driven transactions.",
    "Revenant Protocol AI": "A legendary rogue AI said to hold the key to breaking the balance of power in the Aetherverse.",
}

# 🎲 Skill Check Mechanic
def skill_check(player_skill_level, difficulty):
    roll = random.randint(1, 100)
    return (roll + player_skill_level) >= difficulty, roll

# 📍 Real-Time Player Location Tracking
@socketio.on("update_location")
def update_location(data):
    player_name = data.get("player_name", "")
    new_location = data.get("location", "")

    conn = get_db_connection()
    conn.execute("UPDATE players SET location = ? WHERE name = ?", (new_location, player_name))
    conn.commit()
    conn.close()

    emit("game_response", {"response": f"📍 {player_name} moved to {new_location}."})

# 🔄 Persistent NPC Memory System
@socketio.on("player_npc_interaction")
def handle_npc_interaction(data):
    player_name = data.get("player_name", "")
    npc_name = data.get("npc_name", "")

    conn = get_db_connection()
    npc = conn.execute("SELECT * FROM npcs WHERE name = ?", (npc_name,)).fetchone()
    conn.close()

    if npc:
        response = f"{npc_name} remembers you: {npc['last_interaction']}."
    else:
        response = f"{npc_name} does not seem to know you."

    emit("game_response", {"response": response})

# ⚔️ Turn-Based Combat AI System
@socketio.on("combat_turn")
def handle_combat_turn(data):
    player_name = data.get("player_name", "")
    player_attack = data.get("attack", "")
    player_skill_level = data.get("skill_level", 50)
    enemy_name = "Cyber-Warrior Elite"
    enemy_difficulty = 65

    success, roll = skill_check(player_skill_level, enemy_difficulty)

    if success:
        response = f"✅ {player_name} lands a successful {player_attack} on {enemy_name} (Roll: {roll})."
    else:
        response = f"❌ {player_name} misses! {enemy_name} counterattacks. (Roll: {roll})"

    emit("game_response", {"response": response})

# 🎭 AI-Driven Game Master Response Generator
@socketio.on("chat_message")
def handle_chat_message(data):
    player_message = data.get("message", "").lower()

    for key, value in AETHERPUNK_LORE.items():
        if key.lower() in player_message:
            emit("game_response", {"response": f"📖 {key}: {value}"})
            return

    emit("game_response", {"response": "🔹 The Aetherverse is vast. Be more specific in your request."})

# 🛠️ Flask Routes for Frontend
@app.route("/")
def index():
    return render_template("index.html")

# 🚀 Run the WebSocket Server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=10000)
