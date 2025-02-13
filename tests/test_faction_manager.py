import unittest
from gameplay.faction_manager import Faction

class TestFactionManager(unittest.TestCase):
    """Unit tests for the Faction Manager."""
    
    def setUp(self):
        """Creates a sample faction for testing."""
        self.faction = Faction(
            name="Volthari Council",
            influence=70,
            reputation=10,
            territory=["Helios Wastes"],
            economy=50
        )
    
    def test_faction_initialization(self):
        """Tests that the faction initializes correctly."""
        self.assertEqual(self.faction.name, "Volthari Council")
        self.assertEqual(self.faction.influence, 70)
        self.assertEqual(self.faction.reputation, 10)
        self.assertIn("Helios Wastes", self.faction.territory)
        self.assertEqual(self.faction.economy, 50)
    
    def test_update_reputation(self):
        """Tests updating reputation."""
        self.faction.update_reputation(15)
        self.assertEqual(self.faction.reputation, 25)
    
    def test_change_influence(self):
        """Tests modifying faction influence."""
        self.faction.change_influence(-10)
        self.assertEqual(self.faction.influence, 60)
    
    def test_change_economy(self):
        """Tests modifying faction economy."""
        self.faction.change_economy(5)
        self.assertEqual(self.faction.economy, 55)
    
    def test_form_alliance(self):
        """Tests forming an alliance between factions."""
        other_faction = Faction("Syndicate X", 65, -5, ["Titan Sprawl"], 40)
        result = self.faction.form_alliance(other_faction)
        self.assertIn("Syndicate X", self.faction.alliances)
        self.assertIn("Volthari Council", other_faction.alliances)
        self.assertEqual(result, "Volthari Council has allied with Syndicate X.")
    
    def test_declare_war(self):
        """Tests declaring war on another faction."""
        other_faction = Faction("Pyronax Senate", 80, 0, ["Void District"], 60)
        result = self.faction.declare_war(other_faction)
        self.assertIn("Pyronax Senate", self.faction.enemies)
        self.assertIn("Volthari Council", other_faction.enemies)
        self.assertEqual(result, "Volthari Council has declared war on Pyronax Senate.")

if __name__ == "__main__":
    unittest.main()
