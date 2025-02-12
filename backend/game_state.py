import redis
import json

class GameState:
    """Manages game state in Redis for real-time interactions."""
    
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def save_state(self, player_id, data):
        """Save player state in Redis."""
        self.redis.set(player_id, json.dumps(data))

    def load_state(self, player_id):
        """Load player state from Redis."""
        state = self.redis.get(player_id)
        return json.loads(state) if state else {}

    def update_state(self, player_id, key, value):
        """Update a specific key in the game state."""
        state = self.load_state(player_id)
        state[key] = value
        self.save_state(player_id, state)

    def delete_state(self, player_id):
        """Reset player state."""
        self.redis.delete(player_id)

