import random

class RPGMechanics:
    """Handles skill checks, combat, and hacking mechanics."""

    def skill_check(self, skill_level, difficulty):
        """Performs a skill check against a difficulty threshold."""
        roll = random.randint(1, 20) + skill_level
        return roll >= difficulty

    def combat(self, attacker_stats, defender_stats):
        """Handles turn-based combat between two entities."""
        attack_roll = random.randint(1, 20) + attacker_stats["attack"]
        defense_roll = random.randint(1, 20) + defender_stats["defense"]

        if attack_roll > defense_roll:
            damage = max(1, attacker_stats["damage"] - defender_stats["armor"])
            return {"success": True, "damage": damage}
        return {"success": False, "damage": 0}

    def hacking_attempt(self, hacker_skill, system_security):
        """Performs a hacking attempt against a system."""
        hack_roll = random.randint(1, 20) + hacker_skill
        return hack_roll >= system_security
