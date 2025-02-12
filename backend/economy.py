import random
import json
import redis
from backend.game_state import GameState

class Economy:
    """Manages AI-driven economy, market fluctuations, and black-market trade."""

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)
        self.game_state = GameState()

        self.base_exchange_rates = {
            "AuroCreds": 1.0,
            "NeuroCreds": 1.5,
            "AetherCreds": 3.0,
        }
        
        self.base_prices = {
            "Weapons": 5000,
            "Cyberware": 7000,
            "Armor": 4000,
            "Aurovium (kg)": 12000,
            "Neurovium (kg)": 18000,
        }

    def get_market_prices(self):
        """Returns fluctuating market prices based on AI-driven economic shifts."""
        for item in self.base_prices.keys():
            self.base_prices[item] *= random.uniform(0.9, 1.2)
        return self.base_prices

    def get_exchange_rates(self):
        """Returns fluctuating currency exchange rates based on demand/supply."""
        self.base_exchange_rates["NeuroCreds"] *= random.uniform(0.95, 1.1)
        self.base_exchange_rates["AetherCreds"] *= random.uniform(0.98, 1.05)
        return self.base_exchange_rates
