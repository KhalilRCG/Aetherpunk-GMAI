import openai
import json
import redis
from game_state import GameState

openai.api_key = os.getenv("OPENAI_API_KEY")

class CityBuilder:
    """AI-Driven Procedural City Generation System"""

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.game_state = GameState()
        self.system_prompt = "You are a cyberpunk city-building AI, generating detailed city maps with districts, economic zones, and faction-controlled areas."

    def generate_city(self, player_id):
        """Creates a new AI-generated cyberpunk city based on world events."""
        state = self.game_state.load_state(player_id)
        faction = state.get("affiliated_faction", "Neutral")
        economy = state.get("economy_status", "Stable")

        context = f"""
        - Player Faction Influence: {faction}
        - Economy Status: {economy}
        - Recent Events: {state.get("recent_events", [])}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Generate a detailed cyberpunk city map with districts based on: {context}"}
            ]
        )

        city_data = response["choices"][0]["message"]["content"]
        state["cities"] = state.get("cities", []) + [city_data]
        self.game_state.save_state(player_id, state)

        return city_data
