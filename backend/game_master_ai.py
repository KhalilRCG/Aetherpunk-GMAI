import openai
import os
from city_builder import CityBuilder
from game_state import GameState

openai.api_key = os.getenv("OPENAI_API_KEY")

class GameMasterAI:
    """Handles AI-generated responses for missions, lore, and city-building."""
    
    def __init__(self):
        self.city_builder = CityBuilder()
        self.game_state = GameState()
        self.system_prompt = "You are the Aetherpunk Game Master, generating immersive cyberpunk RPG missions, lore, and city-building data."

    def generate_event(self, player_action, game_state):
        """Generates dynamic responses based on player actions and game state."""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"Player action: {player_action}. Game state: {game_state}"}
            ]
        )
        return response["choices"][0]["message"]["content"]
