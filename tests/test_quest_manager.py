import unittest
from gameplay.quest_manager import Quest, generate_quest

class TestQuestManager(unittest.TestCase):
    """Unit tests for the Quest Manager."""
    
    def setUp(self):
        """Creates a sample quest for testing."""
        self.quest = Quest(
            giver="Darius Coil",
            faction="Syndicate X",
            quest_type="Heist",
            difficulty="Hard",
            objectives=["Break into the vault", "Steal the artifact", "Escape without being detected"],
            rewards="Rare cyberware",
            consequences="Faction hostility increased",
            hidden_objectives=["Retrieve hidden data chip"],
            npc_involvement="Elite guard patrol",
            faction_rival_interference="Rival Syndicate interference",
            branching_paths="Betray employer for a better deal",
            black_market_deals="A fixer offers an alternative reward",
            emergency_extraction="Hidden tunnel escape",
            faction_double_cross="Employer sells out the player",
            faction_negotiation="Rival faction offers a ceasefire",
            hidden_bounty_escalation="Secret bounty placed on player",
            reputation_outcome="Boosts reputation with underground fixers",
            ai_difficulty_adjustment="Increased security measures",
            undercover_infiltration="Disguise required",
            faction_power_shift="Syndicate gains more influence"
        )
    
    def test_quest_initialization(self):
        """Tests that the quest initializes correctly."""
        self.assertEqual(self.quest.giver, "Darius Coil")
        self.assertEqual(self.quest.faction, "Syndicate X")
        self.assertEqual(self.quest.quest_type, "Heist")
        self.assertEqual(self.quest.difficulty, "Hard")
    
    def test_progress_quest(self):
        """Tests quest progression."""
        initial_stage = self.quest.stage
        self.quest.progress_quest()
        self.assertEqual(self.quest.stage, initial_stage + 1)
    
    def test_reveal_hidden_objectives(self):
        """Tests revealing hidden objectives."""
        hidden_objective = self.quest.reveal_hidden_objectives()
        self.assertIn("Retrieve hidden data chip", hidden_objective)
    
    def test_update_status(self):
        """Tests updating quest status."""
        self.quest.update_status("success")
        self.assertEqual(self.quest.status, "Completed")
        
        self.quest.update_status("failure")
        self.assertEqual(self.quest.status, "Failed")

if __name__ == "__main__":
    unittest.main()
