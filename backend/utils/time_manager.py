import datetime
import random

class TimeManager:
    def __init__(self):
        self.current_time = datetime.datetime(2125, 5, 17, 12, 0)  # Starting in-game date and time
        self.time_step = datetime.timedelta(minutes=30)  # Each action advances time by 30 minutes
        self.faction_movements = {
            "morning": ["Corporate security sweeps the streets for rogue hackers.", "Fixers arrange early deals for the day."],
            "afternoon": ["Gangs flex their power in contested districts.", "Mercenaries receive new hit contracts."],
            "evening": ["Black market trade reaches peak hours.", "Elite syndicates conduct high-risk negotiations."],
            "night": ["Cybercriminals launch major hacking raids.", "Rival factions engage in sudden turf wars."]
        }
        self.faction_conflicts = [
            "A long-standing gang rivalry erupts into full-blown street warfare.",
            "Corporate assassins eliminate a high-profile syndicate leader, triggering chaos.",
            "An underground rebellion sparks resistance against oppressive corporate rule.",
            "Smugglers are caught in the crossfire of a growing faction dispute."
        ]
        self.news_headlines = [
            "Breaking: Citywide blackout suspected to be the result of cyberwarfare!",
            "Exclusive: Underground resistance movement gains traction in the lower districts.",
            "Alert: High-tech arms dealer assassinated in broad daylight!",
            "Update: Reports of faction leaders disappearing without a trace."
        ]
        self.economic_fluctuations = [
            "Corporate stock values fluctuate as the black market economy surges.",
            "Weapon prices skyrocket due to escalating gang violence.",
            "Underground cyberware prices plummet as a new supply chain emerges.",
            "Factions struggle for resources as trade routes are disrupted."
        ]
        self.player_influence_events = [
            "Player intervention alters public perception, shifting faction allegiances.",
            "A player's black-market dealings lead to increased surveillance in certain districts.",
            "A major corporate contract is offered to the player due to their notoriety.",
            "Player sabotage disrupts a faction's operations, forcing an emergency response."
        ]
        self.reactive_npc_behaviors = [
            "NPCs start avoiding the player due to their growing infamy.",
            "Merchants offer better deals based on the player's reputation.",
            "Certain factions deploy spies to track the player’s movements.",
            "High-risk NPCs offer secret missions due to the player's influence."
        ]
        self.faction_intelligence_networks = [
            "A faction intercepts rival communications, gaining a strategic advantage.",
            "Undercover operatives infiltrate corporate enclaves to extract critical intel.",
            "A syndicate leaks classified data, exposing hidden operations in the city.",
            "Hackers disrupt government surveillance, obscuring faction activities."
        ]
        self.black_market_fluctuations = [
            "High demand for cybernetic augmentations leads to increased prices.",
            "A sudden crackdown on smuggling forces the market into deeper secrecy.",
            "Rare prototype weapons flood the market after a warehouse heist.",
            "A currency devaluation in the underground economy disrupts trade."
        ]
        self.player_bounty_events = [
            "A bounty is placed on the player by an unknown benefactor.",
            "Mercenaries are now actively hunting the player in certain districts.",
            "A faction increases the bounty on the player's head due to interference.",
            "A rival faction offers the player a deal to remove their bounty."
        ]

    def advance_time(self):
        """Advances the in-game time by the defined time step."""
        self.current_time += self.time_step

    def get_current_time(self):
        """Returns the current in-game time in a formatted string."""
        return self.current_time.strftime("%Y-%m-%d %H:%M")
    
    def is_night(self):
        """Checks if it is currently nighttime in the game world."""
        hour = self.current_time.hour
        return hour < 6 or hour > 18
    
    def get_day_phase(self):
        """Returns the current phase of the day based on in-game time."""
        hour = self.current_time.hour
        if 6 <= hour < 12:
            return "Morning"
        elif 12 <= hour < 18:
            return "Afternoon"
        elif 18 <= hour < 21:
            return "Evening"
        else:
            return "Night"
    
    def get_city_activity(self):
        """Returns a description of city activity based on the time of day."""
        phase = self.get_day_phase().lower()
        return random.choice(self.faction_movements.get(phase, ["The city remains eerily quiet."]))
    
    def get_faction_conflict(self):
        """Randomly generates faction conflict escalations."""
        if random.random() < 0.25:
            return random.choice(self.faction_conflicts)
        return "No major faction conflicts at the moment."
    
    def get_news_report(self):
        """Generates an in-game news headline about current world events and potential player interactions."""
        if random.random() < 0.3:
            return random.choice(self.news_headlines)
        return "No breaking news at this time."
    
    def get_economic_fluctuation(self):
        """Returns a random economic change caused by conflicts and faction movements."""
        if random.random() < 0.25:
            return random.choice(self.economic_fluctuations)
        return "The economy remains stable for now."
    
    def get_player_influence(self):
        """Determines how player actions impact the world, affecting news, factions, and the economy."""
        if random.random() < 0.2:
            return random.choice(self.player_influence_events)
        return "Player actions remain under the radar for now."
    
    def get_npc_reaction(self):
        """Returns NPC behavior changes based on the player's reputation and actions."""
        if random.random() < 0.25:
            return random.choice(self.reactive_npc_behaviors)
        return "NPCs behave as usual."
    
    def get_faction_intelligence_update(self):
        """Returns a random faction intelligence network event."""
        if random.random() < 0.2:
            return random.choice(self.faction_intelligence_networks)
        return "Factions continue gathering intel in secrecy."
    
    def get_black_market_trend(self):
        """Returns a random economic shift in the black market economy."""
        if random.random() < 0.25:
            return random.choice(self.black_market_fluctuations)
        return "Black market economy remains stable for now."
    
    def get_player_bounty_status(self):
        """Determines if a bounty has been placed on the player and its consequences."""
        if random.random() < 0.3:
            return random.choice(self.player_bounty_events)
        return "No active bounties on the player at this time."

if __name__ == "__main__":
    time_manager = TimeManager()
    print(f"Starting Time: {time_manager.get_current_time()} - {time_manager.get_day_phase()} - {time_manager.get_city_activity()} - {time_manager.get_faction_conflict()} - {time_manager.get_news_report()} - {time_manager.get_economic_fluctuation()} - {time_manager.get_player_influence()} - {time_manager.get_npc_reaction()} - {time_manager.get_faction_intelligence_update()} - {time_manager.get_black_market_trend()} - {time_manager.get_player_bounty_status()}")
    time_manager.advance_time()
