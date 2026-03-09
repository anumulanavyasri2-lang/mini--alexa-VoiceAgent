import redis
import json

class MemoryManager:
    def __init__(self, host='localhost', port=6379, db=0):
        # Session Memory: Redis
        self.redis_client = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        # Persistent Memory: Mocked as DB connection usually, here we mock a dict for simplicity
        # Real implementation would use psycopg2 to hit PostgreSQL
        self.persistent_db = {
            "patient_123": {
                "preferred_language": "ta", # Tamil
                "past_appointments": []
            }
        }

    def get_session_state(self, session_id: str) -> dict:
        """Retrieve conversation_state (pending intent, current doctor)"""
        try:
            state_json = self.redis_client.get(session_id)
            if state_json:
                return json.loads(state_json)
        except Exception as e:
            pass # Return default if redis unavailable
        return {"pending_intent": None, "current_doctor": None}

    def update_session_state(self, session_id: str, new_state: dict):
        """
        Memory Bonus: Redis TTL.
        Ensure we set an expiry on the session memory to show horizontal scaling.
        """
        try:
            state_json = json.dumps(new_state)
            self.redis_client.set(session_id, state_json, ex=3600)  # expires in 1 hour
        except Exception as e:
            pass # Fallback for local testing if redis is not running

    def get_patient_profile(self, patient_id: str) -> dict:
        """Persistent Memory retrieval"""
        return self.persistent_db.get(patient_id, {"preferred_language": "en", "past_appointments": []})
