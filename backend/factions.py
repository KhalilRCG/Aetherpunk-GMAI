import random

class Factions:
    """Manages faction reputation, conflicts, and influence mechanics."""

    def __init__(self):
        self.factions = {
            "Red Talons": {"influence": 50, "hostility": 20, "war_status": "Neutral"},
            "Obsidian Circuit": {"influence": 40, "hostility": 30, "war_status": "At Peace"},
            "Volthari Syndicate": {"influence": 60, "hostility": 25, "war_status": "Neutral"}
        }

    def adjust_reputation(self, faction, change):
        """Adjusts faction reputation dynamically."""
        if faction in self.factions:
            self.factions[faction]["influence"] += change

    def start_war(self, faction1, faction2):
        """Triggers war between two factions if hostility is high enough."""
        if (self.factions[faction1]["hostility"] + self.factions[faction2]["hostility"]) > 70:
            self.factions[faction1]["war_status"] = "At War"
            self.factions[faction2]["war_status"] = "At War"
            return f"{faction1} and {faction2} are now at war!"
        return "Tensions are rising, but no war yet."

    def get_faction_status(self, faction):
        """Returns the current status of a faction."""
        return self.factions.get(faction, {})
