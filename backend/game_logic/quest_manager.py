import random
import json
import asyncio
from websockets import broadcast

# Global storage for WebSocket connections
active_connections = set()

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
    
    async def send_update(self, update_message):
        """Sends real-time updates to connected WebSocket clients."""
        if active_connections:
            await broadcast(active_connections, json.dumps({"quest_update": update_message}))
    
    async def progress_quest(self):
        """Advances the quest to the next stage and sends a UI update."""
        self.stage += 1
        if self.stage > len(self.objectives):
            self.status = "Completed"
            await self.send_update(f"Quest '{self.quest_type}' fully completed! Rewards: {self.rewards}, Reputation Impact: {self.reputation_outcome}, Faction Power Shift: {self.faction_power_shift}")
            return
        await self.send_update(f"Stage {self.stage}: {self.objectives[self.stage - 1]}")
    
    async def reveal_hidden_objectives(self):
        """Reveals hidden objectives if conditions are met and sends a UI update."""
        if self.hidden_objectives:
            revealed = self.hidden_objectives.pop(0)
            await self.send_update(f"New Hidden Objective Unlocked: {revealed}")
        else:
            await self.send_update("No hidden objectives remaining.")
    
    async def update_status(self, outcome):
        """Updates the quest status and sends a UI update."""
        if outcome == "success":
            self.status = "Completed"
            await self.send_update(f"Quest '{self.quest_type}' completed. Rewards: {self.rewards}, Reputation Impact: {self.reputation_outcome}, Faction Power Shift: {self.faction_power_shift}")
        elif outcome == "failure":
            if self.emergency_extraction:
                await self.send_update(f"Mission failed, but an emergency extraction saved you: {self.emergency_extraction}")
            self.status = "Failed"
            await self.send_update(f"Quest '{self.quest_type}' failed. Consequences: {self.consequences}, Hidden Bounty Escalation: {self.hidden_bounty_escalation}")
        elif outcome == "betrayal":
            if self.faction_double_cross:
                await self.send_update(f"You were double-crossed by {self.faction}! {self.faction_double_cross}")
            self.status = "Betrayed"
            await self.send_update(f"You betrayed {self.giver}. Faction standing with {self.faction} severely damaged.")

async def connect_websocket(websocket):
    """Handles WebSocket connections for real-time quest updates."""
    active_connections.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        active_connections.remove(websocket)
