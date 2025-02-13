import random
import json
import datetime
from utils.time_manager import TimeManager
from utils.generator import generate_event

class AetherpunkChatbot:
    def __init__(self):
        self.time_manager = TimeManager()
        self.load_data()

    def load_data(self):
        try:
            with open("../data/factions.json", "r") as f:
                self.factions = json.load(f)
            with open("../data/items.json", "r") as f:
                self.items = json.load(f)
            with open("../data/locations.json", "r") as f:
                self.locations = json.load(f)
            with open("../data/npc_profiles.json", "r") as f:
                self.npcs = json.load(f)
            with open("../data/quests.json", "r") as f:
                self.quests = json.load(f)
        except FileNotFoundError as e:
            print(f"Error loading data: {e}")
            self.factions, self.items, self.locations, self.npcs, self.quests = {}, {}, {}, {}, {}

    def generate_response(self, user_input, player_state):
        """
        Generates a dynamic response based on user input, incorporating the cyberpunk tone.
        """
        self.time_manager.advance_time()
        in_game_time = self.time_manager.get_current_time()

        context = self.determine_context(user_input, player_state)
        event = generate_event(player_state, context)
        npc_interaction = self.handle_npc_interaction(player_state, context)
        quest_update = self.update_quest_progress(player_state, context)
        side_quest = self.generate_npc_side_quest(player_state)
        faction_quest = self.generate_faction_quest(player_state)
        undercover_mission = self.generate_undercover_mission(player_state)
        faction_war = self.trigger_faction_war(player_state)
        takeover_attempt = self.attempt_faction_takeover(player_state)
        hidden_agenda = self.reveal_hidden_faction_agenda(player_state)
        faction_resources = self.manage_faction_resources(player_state)
        player_faction = self.create_player_faction(player_state)
        territory_control = self.manage_territory_control(player_state)
        diplomacy = self.handle_diplomatic_negotiations(player_state)
        economic_system = self.manage_faction_economy(player_state)
        cyberwarfare = self.handle_cyberwarfare(player_state)
        experience = self.manage_experience_points(player_state)
        skill_tree = self.handle_skill_tree(player_state)
        skill_synergy = self.apply_skill_synergy(player_state)
        skill_evolution = self.evolve_skills(player_state)
        faction_abilities = self.unlock_faction_abilities(player_state)
        faction_update = self.update_faction_relations(player_state, context)
        faction_perks = self.get_faction_perks(player_state)
        npc_alliance = self.handle_npc_alliance_rivalry(player_state)
        betrayal = self.handle_npc_betrayal(player_state)

        responses = [
            f"The neon lights flicker overhead as the city hums with restless energy. You say: '{user_input}'.", 
            f"A distant siren wails as you weigh your choices. '{user_input}'—let's see where this leads...",
            f"A rogue drone scans the area, its red eye gleaming. Your words '{user_input}' echo in the urban sprawl..."
        ]
        
        response = random.choice(responses) + f" [In-game time: {in_game_time}]"
        return response + f"\n{event}\n{npc_interaction}\n{quest_update}\n{side_quest}\n{faction_quest}\n{undercover_mission}\n{faction_war}\n{takeover_attempt}\n{hidden_agenda}\n{faction_resources}\n{player_faction}\n{territory_control}\n{diplomacy}\n{economic_system}\n{cyberwarfare}\n{experience}\n{skill_tree}\n{skill_synergy}\n{skill_evolution}\n{faction_abilities}\n{faction_update}\n{faction_perks}\n{npc_alliance}\n{betrayal}"  
    
    def determine_context(self, user_input, player_state):
        """
        Determines the context of the user input.
        """
        keywords = {
            "combat": ["attack", "fight", "draw weapon", "shoot"],
            "trade": ["buy", "sell", "trade", "negotiate"],
            "exploration": ["travel", "move", "explore", "navigate"],
            "dialogue": ["talk", "speak", "ask", "question"],
            "quest": ["mission", "job", "task", "objective"]
        }
        
        for category, words in keywords.items():
            if any(word in user_input.lower() for word in words):
                return category
        
        return "general"
    
    def handle_npc_interaction(self, player_state, context):
        """
        Determines NPC interactions based on context and player actions.
        """
        if context == "dialogue":
            npc = random.choice(list(self.npcs.keys())) if self.npcs else "Unknown NPC"
            return f"{npc} responds to your approach, their cybernetic eye glinting under the neon lights."
        return ""
    
if __name__ == "__main__":
    chatbot = AetherpunkChatbot()
    while True:
        user_input = input("\n> ")
        player_state = {
            "reputation": {}, "quest_progress": {}, "faction_reputation": {}, "influence": 0, 
            "experience_points": 0, "attribute_points": 0, "skill_points": 0, "level": 1, "archetype": "mercenary"
        }  # Placeholder for player state
        print(chatbot.generate_response(user_input, player_state))
