from dataclasses import dataclass, field
import uuid, random
from typing import List, Dict, Any

@dataclass
class SeedWorld:
    id: str
    domain: str
    goal: str
    difficulty: float
    noise: float
    mutation_rate: float
    constraints: List[str]
    roles: List[str]
    meta: Dict[str, Any] = field(default_factory=dict)

class SeedEngine:
    def __init__(self, global_seed: int | None = None):
        self.global_seed = global_seed or random.randint(1, 10000)
        self.rng = random.Random(self.global_seed)

    def generate(self, domain: str, goal: str, template: dict | None = None) -> SeedWorld:
        template = template or {}
        return SeedWorld(
            id=str(uuid.uuid4()),
            domain=domain,
            goal=goal,
            difficulty=template.get("difficulty", 0.5),
            noise=template.get("noise", 0.1),
            mutation_rate=template.get("mutation_rate", 0.1),
            constraints=template.get("constraints", []),
            roles=template.get("roles", ["planner", "builder", "critic", "verifier"]),
            meta={"seed": self.global_seed}
        )