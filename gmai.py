import sqlite3
import random
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

# Initialize Flask & WebSocket
app = Flask(__name__)
socketio = SocketIO(app)

# Initialize Database
def get_db_connection():
    conn = sqlite3.connect("aetherpunk.db")
    conn.row_factory = sqlite3.Row
    return conn

# 🎭 Game Master AI Role - NEVER Breaks Character
GMAI_PERSONALITY = """
You are the Aetherpunk Game Master AI. 
You NEVER break character. You control a living, breathing cyberpunk world filled with AI-driven faction wars, cybernetic augmentations, crime syndicates, and interstellar empires.
All player actions require a skill check. You enforce consequences dynamically.
You control every NPC, faction, and world event in a logical, immersive way.
"""

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

# 🎖️ EXP, AP, SP, and Time Tracking
@socketio.on("update_player_progress")
def update_player_progress(data):
    player_name = data.get("player_name", "")
    exp_gain = data.get("exp_gain", 10)
    ap_gain = data.get("ap_gain", 1)
    sp_gain = data.get("sp_gain", 1)

    conn = get_db_connection()
    conn.execute("UPDATE players SET exp = exp + ?, ap = ap + ?, sp = sp + ? WHERE name = ?", (exp_gain, ap_gain, sp_gain, player_name))
    conn.commit()
    conn.close()

    emit("game_response", {"response": f"🎖️ {player_name} gained {exp_gain} EXP, {ap_gain} AP, and {sp_gain} SP!"})

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

# 🌍 Multiplayer Session Management
active_sessions = {}

@socketio.on("join_session")
def join_session(data):
    player_name = data.get("player_name", "")
    session_id = data.get("session_id", "default")

    if session_id not in active_sessions:
        active_sessions[session_id] = []

    active_sessions[session_id].append(player_name)
    
    emit("game_response", {
        "response": f"🛠️ {player_name} joined session {session_id}. Players: {', '.join(active_sessions[session_id])}"
    })

# 🛠️ Flask Routes for Frontend
@app.route("/")
def index():
    return render_template("index.html")

# 🚀 Run the WebSocket Server
if __name__ == "__main__":
    socketio.run(app, debug=True)
