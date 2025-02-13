import random

class Quest:
    """Represents a quest dynamically generated based on player interactions and world conditions."""
    def __init__(self, giver, faction, quest_type, difficulty, objectives, rewards, consequences, hidden_objectives, npc_involvement, faction_rival_interference, branching_paths, black_market_deals, emergency_extraction, faction_double_cross, faction_negotiation, hidden_bounty_escalation, reputation_outcome, ai_difficulty_adjustment, undercover_infiltration, faction_power_shift):
        self.giver = giver  # NPC who assigns the quest
        self.faction = faction  # Associated faction
        self.quest_type = quest_type  # Assassination, Heist, Espionage, Trade, etc.
        self.difficulty = difficulty  # Scale of difficulty (Easy, Medium, Hard, Deadly)
        self.objectives = objectives  # List of mission objectives
        self.hidden_objectives = hidden_objectives  # Hidden objectives that are revealed later
        self.rewards = rewards  # Rewards upon completion
        self.consequences = consequences  # Outcomes of failure or betrayal
        self.npc_involvement = npc_involvement  # NPCs dynamically involved in the mission
        self.faction_rival_interference = faction_rival_interference  # Events where rival factions interfere with the quest
        self.branching_paths = branching_paths  # Different quest paths based on player choices
        self.black_market_deals = black_market_deals  # Underground opportunities that affect mission outcomes
        self.emergency_extraction = emergency_extraction  # Special escape plans in case of mission failure
        self.faction_double_cross = faction_double_cross  # Potential backstabs by the hiring faction
        self.faction_negotiation = faction_negotiation  # Dynamic faction diplomacy that alters quest conditions
        self.hidden_bounty_escalation = hidden_bounty_escalation  # Bounties that increase based on hidden triggers
        self.reputation_outcome = reputation_outcome  # How the quest completion affects the player's reputation
        self.ai_difficulty_adjustment = ai_difficulty_adjustment  # AI dynamically scales mission difficulty
        self.undercover_infiltration = undercover_infiltration  # Player goes undercover to complete a mission
        self.faction_power_shift = faction_power_shift  # Faction influence changes based on quest outcome
        self.status = "Active"  # Quest status: Active, Completed, Failed
        self.stage = 1  # Multi-stage quest progression
    
    def progress_quest(self):
        """Advances the quest to the next stage."""
        self.stage += 1
        if self.stage > len(self.objectives):
            self.status = "Completed"
            return f"Quest '{self.quest_type}' fully completed! Rewards: {self.rewards}, Reputation Impact: {self.reputation_outcome}, Faction Power Shift: {self.faction_power_shift}"
        return f"Stage {self.stage}: {self.objectives[self.stage - 1]}"

    def reveal_hidden_objectives(self):
        """Reveals hidden objectives if conditions are met."""
        if self.hidden_objectives:
            revealed = self.hidden_objectives.pop(0)
            return f"New Hidden Objective Unlocked: {revealed}"
        return "No hidden objectives remaining."
    
    def update_status(self, outcome):
        """Updates the quest status based on player actions."""
        if outcome == "success":
            self.status = "Completed"
            return f"Quest '{self.quest_type}' completed. Rewards: {self.rewards}, Reputation Impact: {self.reputation_outcome}, Faction Power Shift: {self.faction_power_shift}"
        elif outcome == "failure":
            if self.emergency_extraction:
                return f"Mission failed, but an emergency extraction saved you: {self.emergency_extraction}"
            self.status = "Failed"
            return f"Quest '{self.quest_type}' failed. Consequences: {self.consequences}, Hidden Bounty Escalation: {self.hidden_bounty_escalation}"
        elif outcome == "betrayal":
            if self.faction_double_cross:
                return f"You were double-crossed by {self.faction}! {self.faction_double_cross}"
            self.status = "Betrayed"
            return f"You betrayed {self.giver}. Faction standing with {self.faction} severely damaged."
        return "No changes to quest status."


def generate_quest(player_reputation, faction_affiliation):
    """Dynamically generates a quest based on the player's reputation and faction."""
    quest_givers = ["Kara Vex", "Darius Coil", "Echo Nyx", "Victor Graves", "Sable Wren"]
    quest_types = ["Assassination", "Heist", "Espionage", "Trade Deal", "Escort", "Sabotage"]
    difficulties = ["Easy", "Medium", "Hard", "Deadly"]
    
    ai_difficulty_adjustments = ["Enemy reinforcements arrive", "Security measures are increased", "A surprise twist alters the mission objectives"]
    undercover_infiltrations = ["Player must assume a false identity", "Mission requires deep cover tactics", "A mole inside the target faction aids the player"]
    faction_power_shifts = ["Faction influence expands due to mission success", "A rival faction loses territory", "Political control changes hands"]
    
    giver = random.choice(quest_givers)
    quest_type = random.choice(quest_types)
    difficulty = random.choice(difficulties)
    faction = faction_affiliation if faction_affiliation else random.choice(["Corporate", "Syndicate", "Resistance", "Freelancer"])
    
    return Quest(
        giver=giver,
        faction=faction,
        quest_type=quest_type,
        difficulty=difficulty,
        objectives=random.sample(["Primary objective secured", "Secondary targets neutralized", "Intel recovered"], k=3),
        hidden_objectives=random.sample(["Find an unknown informant", "Destroy extra evidence", "Secure encrypted files"], k=2),
        rewards=random.choice(["Rare cyberware", "Faction influence boost", "High-value credits", "Advanced weapon mods"]),
        consequences=random.choice(["Faction hostility increased", "Bounty placed on your head", "Rival NPCs begin hunting you"]),
        npc_involvement=random.choice(["Local gang leader", "Corporate spy", "Elite assassin", "Undercover agent", "Bounty hunter"]),
        faction_rival_interference=random.choice(["A rival faction ambushes the mission", "Enemy spies attempt to sabotage the operation"]),
        branching_paths=random.choice(["Betray your employer for better rewards", "Align with an unexpected ally", "Change the mission goal mid-way"]),
        black_market_deals=random.choice(["A secret fixer offers alternative rewards", "Black-market traders provide hidden mission perks"]),
        emergency_extraction=random.choice(["A covert pilot awaits in a hidden getaway vehicle", "A hidden underground tunnel offers an escape route"]),
        faction_double_cross=random.choice(["Your faction sells you out to the highest bidder", "The employer leaks your location to the authorities"]),
        faction_negotiation=random.choice(["Factions agree to a temporary ceasefire", "A faction changes its demand mid-mission", "A rival faction attempts to recruit you"]),
        hidden_bounty_escalation=random.choice(["Your actions secretly raise your bounty", "A high-profile target places a contract on your head"]),
        reputation_outcome=random.choice(["Boosts reputation with allies", "Severely damages standing with rivals", "Draws the attention of powerful NPCs"]),
        ai_difficulty_adjustment=random.choice(ai_difficulty_adjustments),
        undercover_infiltration=random.choice(undercover_infiltrations),
        faction_power_shift=random.choice(faction_power_shifts)
    )
