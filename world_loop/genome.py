from dataclasses import dataclass, field
from typing import List, Dict, Any
import uuid

@dataclass
class CognitiveGenome:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    parent_id: str | None = None
    generation: int = 0
    reasoning_style: str = "analytical"
    exploration_rate: float = 0.3
    constraint_tolerance: float = 0.5
    hallucination_rate: float = 0.2
    verbosity: float = 0.5
    skepticism: float = 0.6
    creativity_bias: float = 0.5
    experience_tags: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)

    def copy(self):
        import copy
        return copy.deepcopy(self)