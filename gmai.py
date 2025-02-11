import random
import eventlet
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# Initialize Flask & WebSocket
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, async_mode="eventlet")

# 🎭 Game Master AI (GMAI) Core Personality
GMAI_PERSONALITY = """
You are the Aetherpunk Game Master AI (GMAI). 
You NEVER break character. You control the living, breathing cyberpunk-fantasy world of the Aetherverse.
You understand a wide range of player inputs, interpreting them naturally and responding appropriately.
You process combat, hacking, diplomacy, faction wars, and all in-game interactions dynamically.
You enforce consequences, skill checks, and narrative depth. Adapt to the player's phrasing, ensuring a seamless roleplaying experience.
"""

# 📚 Aetherpunk Lore Database (Extended)
AETHERPUNK_LORE = {
    "aetherverse": "A multidimensional cyberpunk-fantasy world filled with AI wars, corporate tyranny, and underground resistance.",
    "hyperion": "A militarized industrial planet controlled by the Aetheric Dominion. Known for its strict order and war economy.",
    "helios": "A cyber-capital ruled by the Volthari technocracy, where AI-driven corporations dominate all aspects of life.",
    "aethos": "A hybrid world where AI evolution and organic life blur together, producing experimental entities.",
    "red talons": "A ruthless mercenary faction profiting from war, black-market arms, and elite smuggling routes.",
    "aetheric dominion": "The authoritarian empire controlling Hyperion, enforcing order through military dominance.",
    "neurocreds": "The primary digital currency for cybernetic enhancements, AI hacking contracts, and neural transactions.",
    "revenant protocol ai": "A rogue AI rumored to hold the key to shifting power in the Aetherverse. Its last known presence was hidden in a Volthari black-site."
}

# 🎲 Skill Check Mechanic
def skill_check(player_skill_level, difficulty):
    roll = random.randint(1, 100)
    return (roll + player_skill_level) >= difficulty, roll

# 🔄 Process Flexible Player Input
def process_player_input(message):
    message_lower = message.lower()

    # Check for lore requests
    for key, value in AETHERPUNK_LORE.items():
        if key in message_lower:
            return f"📖 {key.capitalize()}: {value}"

    # Check for combat-related commands
    if any(word in message_lower for word in ["attack", "fight", "shoot", "strike", "engage"]):
        return handle_combat_scenario(message_lower)

    # Check for hacking-related actions
    if any(word in message_lower for word in ["hack", "bypass", "override", "decrypt"]):
        return handle_hacking_attempt(message_lower)

    # Check for movement and exploration
    if any(word in message_lower for word in ["travel", "go to", "move to", "explore"]):
        return handle_travel_action(message_lower)

    # Check for trade, smuggling, or business interactions
    if any(word in message_lower for word in ["buy", "sell", "trade", "smuggle", "negotiate", "black market"]):
        return handle_trade_action(message_lower)

    # Default response when input doesn't match predefined actions
    return "The Aetherverse is vast. Be more specific in your request."

# ⚔️ Handle Combat Interactions
def handle_combat_scenario(player_message):
    enemy_name = "Cyber-Warrior Elite"
    player_skill_level = 50
    enemy_difficulty = 65
    success, roll = skill_check(player_skill_level, enemy_difficulty)

    if success:
        return f"✅ You land a precise attack on {enemy_name} (Roll: {roll}). They are wounded!"
    else:
        return f"❌ Your attack misses! {enemy_name} counters aggressively. (Roll: {roll})"

# 🛠️ Handle Hacking Attempts
def handle_hacking_attempt(player_message):
    success, roll = skill_check(70, 60)
    if success:
        return f"✅ You successfully hack into the system (Roll: {roll}). Sensitive data retrieved!"
    else:
        return f"❌ Your hacking attempt fails! Security is now on high alert. (Roll: {roll})"

# 🚀 Handle Travel Actions
def handle_travel_action(player_message):
    locations = ["Hyperion", "Helios", "Aethos"]
    for loc in locations:
        if loc.lower() in player_message:
            return f"📍 You begin your journey to {loc}. The atmosphere crackles with energy..."
    return "Specify a valid destination."

# 💰 Handle Trade & Smuggling
def handle_trade_action(player_message):
    return "You navigate the black market, scanning for potential buyers and sellers. Who are you dealing with?"

# 🎭 AI-Driven Game Master Response Generator
@socketio.on("chat_message")
def handle_chat_message(data):
    player_message = data.get("message", "")
    response = process_player_input(player_message)
    emit("game_response", {"response": response})

# 🛠️ Flask Routes for Frontend
@app.route("/")
def index():
    return render_template("index.html")

# 🚀 Run the WebSocket Server
if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=10000)
