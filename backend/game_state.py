import redis
import json

class GameState:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def save_state(self, player_id, data):
        self.redis.set(player_id, json.dumps(data))

    def load_state(self, player_id):
        state = self.redis.get(player_id)
        return json.loads(state) if state else {}

    def update_state(self, player_id, key, value):
        state = self.load_state(player_id)
        state[key] = value
        self.save_state(player_id, state)

    def delete_state(self, player_id):
        self.redis.delete(player_id)
