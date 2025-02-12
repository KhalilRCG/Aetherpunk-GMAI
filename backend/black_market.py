import random
import redis
from backend.game_state import GameState

class BlackMarket:
    """Handles underground economy, smuggling, and laundering mechanics."""

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.game_state = GameState()
        self.market_prices = {
            "Weapons": random.randint(5000, 15000),
            "Cyberware": random.randint(7000, 20000),
            "Aurovium (kg)": random.randint(10000, 30000),
            "Neurovium (kg)": random.randint(15000, 35000),
            "Laundered Credits": random.uniform(0.7, 0.95)  # Percentage of money recovered
        }

    def trade(self, item, amount):
        """Processes an underground market trade."""
        if item in self.market_prices:
            return amount * self.market_prices[item]
        return "Invalid Item"

    def launder_money(self, dirty_money):
        """Converts black-market credits into usable currency."""
        return dirty_money * self.market_prices["Laundered Credits"]

    def smuggle_goods(self, item, risk_factor):
        """Smuggles goods with a risk-based success chance."""
        success = random.random() > risk_factor  # Lower risk increases success
        return {
            "success": success,
            "message": "Smuggling successful!" if success else "Smuggling failed! Authorities intercepted shipment."
        }
