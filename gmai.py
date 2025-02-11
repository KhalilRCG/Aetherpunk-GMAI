import random
import eventlet
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

# Initialize Flask & WebSocket
app = Flask(__name__)
socketio = SocketIO(app, async_mode="eventlet")

# Database Connection Function (Corrected SQLite Handling)
def get_db_connection():
    import sqlite3  # Ensures sqlite3 only loads when needed
    conn = sqlite3.connect("aetherpunk.db")
    conn.row_factory = sqlite3.Row
    return conn

# 🎭 Game Master AI Personality - NEVER Breaks Character
GMAI_PERSONALITY = """
You are the Aetherpunk Game Master AI. 
You NEVER break character. You control a living, breathing cyberpunk world filled with AI-driven faction wars, cybernetic augmentations, crime syndicates, and interstellar empires.
All player actions require a skill check. You enforce consequences dynamically.
You control every NPC, faction, and world event in a logical, immersive way.
"""
# 🎭 AI-Driven Game Master Response Generator
def generate_game_response(player_message):
    """Dynamically generates an in-character response based on Aetherpunk lore."""
    lower_message = player_message.lower()

    # Check if the message contains lore-related terms
    for key, value in AETHERPUNK_LORE.items():
        if key.lower() in lower_message:
            return f"📖 {key}: {value}"
    
    # Default response if no lore match is found
    return "The world of Aetherpunk is vast. If you seek knowledge, be more specific."
@socketio.on("chat_message")
def handle_chat_message(data):
    player_message = data.get("message", "")

    # Prevent breaking character
    if any(word in player_message.lower() for word in ["real world", "break character", "not a game"]):
        emit("game_response", {
            "response": "⛔ ERROR: You are within Aetherpunk. There is no real world. Stay in character."
        })
        return

    # Generate immersive response using lore module
    game_master_response = f"📜 {GMAI_PERSONALITY}\n\n🔹 You asked: '{player_message}'\n\n🔹 Game Master says: {generate_game_response(player_message)}"
    
    emit("game_response", {"response": game_master_response})

# 📚 Aetherpunk Lore Database (Predefined World Details)
AETHERPUNK_LORE = {
    "Aetherverse": "The Aetherverse is a cyberpunk-fantasy universe where advanced AI, cybernetic augmentations, interstellar warfare, and black-market trade dominate. The balance between order and chaos is constantly shifting due to conflicts between megacorporations, rogue AI, and underground resistance groups.",
    
    # 🌍 Planets
    "Hyperion": "Hyperion is the militarized industrial powerhouse of the Aetherverse, controlled by the Aetheric Dominion. It is known for its weapon manufacturing hubs, war-torn districts, and highly regulated economy.",
    "Helios": "Helios is the neural cyber capital, dominated by the Volthari technocracy. A city-wide network of augmented minds and AI-driven corporations governs its cyberpunk sprawl.",
    "Aethos": "A mysterious hybrid world, home to Aetherion experimentation. It serves as the link between pure AI and organic life, with deep black-market dealings in cybernetic and Aetheric technology.",
    
    # 🏢 Factions
    "Aetheric Dominion": "The authoritarian rulers of Hyperion, maintaining strict order and controlling military technology with an iron grip. Led by Aetherus, a being infused with Aetheric energy.",
    "Volthari Technocracy": "A council of cybernetic minds that rule Helios, seeking the perfect union between man and machine.",
    "The Old Guard": "A rising black-market syndicate dealing in high-end cybernetics, AI warfare, and underground smuggling. Founded by Vaedros Kyron, Kain Voss, and Veyna Stryx.",
    "Red Talons": "A ruthless mercenary faction that profits from interstellar conflicts and weapons trafficking. They operate under Krynn Vasrek, a feared but strategic warlord.",
    
    # ⚔️ Combat Enhancements
    "Cyberware": "Cybernetic enhancements in the Aetherverse range from basic neural uplinks to full AI-driven augmentation suites. Many illegal upgrades allow for enhanced combat abilities but risk system corruption.",
    "Railstorm Heavy Cannons": "High-impact rail technology designed for corporate security forces and warlords alike. Devastating against armored targets.",
    "Specter Override Key": "A hacking tool capable of hijacking enemy AI-controlled systems for 3 minutes.",
    
    # ⚖️ Economy & Black Market
    "AuroCreds": "The primary currency for physical transactions, often tied to military-industrial complexes.",
    "NeuroCreds": "A digital currency used in high-end cybernetic trade, AI deals, and neural hacking networks.",
    "AetherCreds": "The rarest and most valuable currency, tied to experimental Aetheric technology and AI singularity research.",
    
    # 🛠️ Advanced Technology
    "Revenant Protocol AI": "A legendary rogue AI said to hold the key to breaking the balance of power in the Aetherverse. Its last known traces were encrypted within a Volthari black-site network."
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

# 🎖️ EXP, AP, SP, and Time Tracking
@socketio.on("update_player_progress")
def update_player_progress(data):
    player_name = data.get("player_name", "")
    exp_gain = data.get("exp_gain", 10)
    ap_gain = data.get("ap_gain", 1)
    sp_gain = data.get("sp_gain", 1)

    conn = get_db_connection()
    conn.execute("UPDATE players SET exp = exp + ?, ap = ap + ?, sp = sp + ? WHERE name = ?", 
                 (exp_gain, ap_gain, sp_gain, player_name))
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
    socketio.run(app, debug=True, host="0.0.0.0", port=10000)

