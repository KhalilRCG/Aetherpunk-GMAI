import random

class NPC:
    """Represents an NPC with unique traits, behavior, and dynamic interactions."""
    def __init__(self, name, faction, personality, reputation, role):
        self.name = name
        self.faction = faction
        self.personality = personality  # Aggressive, Diplomatic, Deceptive, Neutral
        self.reputation = reputation  # How they perceive the player
        self.role = role  # Merchant, Fixer, Mercenary, Informant, etc.
        self.memory = {}  # Tracks past interactions with the player
        self.relationship = 0  # Relationship progression with the player
        self.faction_influence = random.randint(1, 100)  # Influence within their faction
        self.betrayal_threshold = random.randint(-50, -20)  # If relationship drops below this, betrayal occurs
        self.hidden_agenda = random.choice(["Power Grab", "Personal Vendetta", "Secret Deal", "Unknown Motivation"])
        self.allegiance_shift_threshold = random.randint(30, 70)  # Relationship level at which NPC may change sides
        self.alliances = set()  # Tracks dynamic NPC alliances

    def interact(self, player_reputation):
        """Determines how the NPC interacts with the player based on reputation and personality."""
        if self.relationship < self.betrayal_threshold:
            return f"{self.name} has betrayed you! Expect consequences."
        
        if self.relationship > self.allegiance_shift_threshold:
            return f"{self.name} has shifted allegiance and now supports you over their original faction."
        
        if self.personality == "Aggressive":
            if player_reputation < -50:
                return f"{self.name} glares at you, hand twitching near their weapon. 'We got unfinished business, punk.'"
            return f"{self.name} sizes you up, smirking. 'You better not waste my time.'"
        
        elif self.personality == "Diplomatic":
            if player_reputation > 50:
                return f"{self.name} greets you warmly. 'Always good to see an ally.'"
            return f"{self.name} nods cautiously. 'Let's talk business, see if we can work something out.'"
        
        elif self.personality == "Deceptive":
            return f"{self.name} grins slyly. 'I got something you might like... but at a price.'"
        
        return f"{self.name} watches you silently, their intentions unreadable."
    
    def update_memory(self, player_action, outcome):
        """Stores past interactions with the player and updates relationship progression."""
        self.memory[player_action] = outcome
        if outcome == "positive":
            self.relationship += 10
        elif outcome == "negative":
            self.relationship -= 10
    
    def form_alliance(self, other_npc):
        """Forms a dynamic alliance with another NPC."""
        if other_npc.name not in self.alliances:
            self.alliances.add(other_npc.name)
            other_npc.alliances.add(self.name)
            return f"{self.name} has formed an alliance with {other_npc.name}."
        return f"{self.name} and {other_npc.name} are already allied."
    
    def break_alliance(self, other_npc):
        """Breaks an existing alliance with another NPC."""
        if other_npc.name in self.alliances:
            self.alliances.remove(other_npc.name)
            other_npc.alliances.remove(self.name)
            return f"{self.name} has severed ties with {other_npc.name}."
        return f"{self.name} has no alliance with {other_npc.name}."
    
    def generate_quest(self, player_reputation):
        """Generates a quest or contract based on the NPC's role, reputation, and faction influence."""
        if self.relationship < self.betrayal_threshold:
            return f"{self.name} set a trap for you. Proceed with caution."
        
        if self.faction_influence > 75:
            high_stakes_mission = f"{self.name}, a high-ranking {self.faction} figure, offers you a crucial mission."
        else:
            high_stakes_mission = f"{self.name} has a small but interesting job for you."
        
        if self.role == "Fixer":
            return f"{high_stakes_mission} 'Got a high-value target that needs to disappear. You in?'"
        elif self.role == "Merchant":
            return f"{high_stakes_mission} 'Rare cyberware just came in. Interested?'"
        elif self.role == "Informant":
            return f"{high_stakes_mission} 'Word on the street is something big's going down soon.'"
        elif self.role == "Mercenary":
            return f"{high_stakes_mission} 'You got enemies. I got solutions.'"
        return f"{self.name} shrugs. 'Nothing for you today. Try again later.'"
    

def generate_npc():
    """Creates a random NPC with varying traits."""
    names = ["Kara Vex", "Darius Coil", "Echo Nyx", "Victor Graves", "Sable Wren"]
    factions = ["Corporate", "Syndicate", "Resistance", "Freelancer"]
    personalities = ["Aggressive", "Diplomatic", "Deceptive", "Neutral"]
    roles = ["Fixer", "Merchant", "Mercenary", "Informant"]
    
    name = random.choice(names)
    faction = random.choice(factions)
    personality = random.choice(personalities)
    reputation = random.randint(-100, 100)
    role = random.choice(roles)
    
    return NPC(name, faction, personality, reputation, role)

if __name__ == "__main__":
    player_reputation = random.randint(-100, 100)
    npc1 = generate_npc()
    npc2 = generate_npc()
    print(f"Encountered NPC: {npc1.name}, Faction: {npc1.faction}, Role: {npc1.role}, Personality: {npc1.personality}, Influence: {npc1.faction_influence}, Hidden Agenda: {npc1.hidden_agenda}")
    print(npc1.interact(player_reputation))
    print(npc1.generate_quest(player_reputation))
    print(npc1.form_alliance(npc2))
    print(npc1.break_alliance(npc2))
