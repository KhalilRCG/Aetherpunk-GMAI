import openai
import json
import redis
from backend.game_state import GameState

openai.api_key = os.getenv("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")

class QuestEngine:
    """AI-Powered Quest System that adapts dynamically based on player choices."""

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.game_state = GameState()
        self.system_prompt = "You are a cyberpunk quest generator, crafting dynamic missions that evolve based on player actions and the shifting game world."

    def generate_quest(self, player_id):
        """Creates a unique AI-generated quest based on the player's current world state."""
        state = self.game_state.load_state(player_id)
        player_faction = state.get("affiliated_faction", "Neutral")
        reputation = state.get("reputation", 0)
        credits = state.get("credits", {"AuroCreds": 0})

        context = f"""
        - Player Faction: {player_faction}
        - Reputation Level: {reputation}
        - Credits: {credits}
        - Previous Quests: {state.get("previous_quests", [])}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Generate a unique cyberpunk quest based on: {context}"}
            ]
        )

        quest = response["choices"][0]["message"]["content"]

        state["current_quest"] = quest
        self.game_state.save_state(player_id, state)

        return quest

    def complete_quest(self, player_id, success=True):
        """Finalizes a quest, updating player stats and world events based on the outcome."""
        state = self.game_state.load_state(player_id)
        quest = state.get("current_quest", "No active quest.")
        
        if success:
            reward = {
                "AuroCreds": 1000,
                "NeuroCreds": 500,
                "Faction Influence": 5
            }
        else:
            reward = {
                "AuroCreds": 0,
                "NeuroCreds": 0,
                "Faction Influence": -10
            }

        state["previous_quests"] = state.get("previous_quests", []) + [quest]
        state["credits"]["AuroCreds"] += reward["AuroCreds"]
        state["credits"]["NeuroCreds"] += reward["NeuroCreds"]
        state["reputation"] += reward["Faction Influence"]

        del state["current_quest"]
        self.game_state.save_state(player_id, state)

        return {"message": "Quest completed.", "reward": reward}
