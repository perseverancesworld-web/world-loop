from typing import Dict, Any

class InMemoryStore:
    def __init__(self):
        self.data: Dict[str, Dict[str, Any]] = {}

    def save_run(self, world_id: str, run_id: str, payload: Dict[str, Any]):
        self.data.setdefault(world_id, {})[run_id] = payload

    def get_history(self, world_id: str):
        return self.data.get(world_id, {})