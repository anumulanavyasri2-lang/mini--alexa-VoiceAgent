import redis
import json

class SessionMemoryClient:
    def __init__(self, host='localhost', port=6379, db=0):
        # Redis mapped to session state
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def get_session_state(self, session_id: str) -> dict:
        """Retrieve conversation_state (pending intent, current doctor, etc.) from memory"""
        state_json = self.redis_client.get(session_id)
        if state_json:
            return json.loads(state_json)
        # Default state
        return {"pending_intent": None, "current_doctor": None, "preferred_language": "en"}

    def update_session_state(self, session_id: str, new_state: dict):
        """
        Memory Bonus: Horizontal Scaling
        We implement a Redis TTL (Time-To-Live). This ensures that stale 
        conversational sessions expire, saving backend memory resources automatically.
        """
        state_json = json.dumps(new_state)
        # Setting expiration to 3600 seconds (1 hour)
        self.redis_client.set(session_id, state_json, ex=3600)
