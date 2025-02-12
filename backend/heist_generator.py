import openai
import json
import redis
from game_state import GameState

openai.api_key = os.getenv("OPENAI_API_KEY")

class HeistGenerator:
    """AI-Powered Heist Generator for cyberpunk RPG missions."""

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.game_state = GameState()
        self.system_prompt = "You are an expert cyberpunk heist planner, creating multi-step heist missions with risk and reward calculations."

    def generate_heist(self, player_id):
        """Creates a multi-step AI-generated heist plan based on player reputation and assets."""
        state = self.game_state.load_state(player_id)
        reputation = state.get("reputation", 0)
        faction_relations = state.get("faction_relations", {})

        context = f"""
        - Player Reputation: {reputation}
        - Faction Relations: {faction_relations}
        - Recent Crimes: {state.get("recent_heists", [])}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Generate a cyberpunk heist with risk assessment based on: {context}"}
            ]
        )

        heist_plan = response["choices"][0]["message"]["content"]
        state["active_heist"] = heist_plan
        self.game_state.save_state(player_id, state)

        return heist_plan

    def complete_heist(self, player_id, success=True):
        """Finalizes a heist, updating player stats based on the outcome."""
        state = self.game_state.load_state(player_id)
        heist = state.get("active_heist", "No active heist.")

        if success:
            reward = {
                "AuroCreds": 20000,
                "NeuroCreds": 10000,
                "Faction Influence": 15
            }
        else:
            reward = {
                "AuroCreds": 0,
                "NeuroCreds": 0,
                "Faction Influence": -20
            }

        state["previous_heists"] = state.get("previous_heists", []) + [heist]
        state["credits"]["AuroCreds"] += reward["AuroCreds"]
        state["credits"]["NeuroCreds"] += reward["NeuroCreds"]
        state["reputation"] += reward["Faction Influence"]

        del state["active_heist"]
        self.game_state.save_state(player_id, state)

        return {"message": "Heist completed.", "reward": reward}
