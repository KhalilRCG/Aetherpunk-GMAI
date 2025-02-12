import openai
import os
import json

openai.api_key = os.getenv("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")

class NPC_AI:
    """AI-powered NPC personalities that evolve based on player interactions."""
    
    def __init__(self):
        self.npc_memory = {}

    def interact(self, npc_name, player_id, interaction):
        """Generates NPC dialogue & learns from past interactions."""
        if npc_name not in self.npc_memory:
            self.npc_memory[npc_name] = {}

        npc_history = self.npc_memory[npc_name].get(player_id, "No previous interactions.")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are {npc_name}, a cyberpunk NPC with deep personality traits."},
                {"role": "user", "content": f"Previous history: {npc_history}. Player interaction: {interaction}"}
            ]
        )

        npc_reply = response["choices"][0]["message"]["content"]
        self.npc_memory[npc_name][player_id] = npc_reply

        return npc_reply
