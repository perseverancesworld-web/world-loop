from abc import ABC, abstractmethod
from typing import Dict, Any
import random

class Benchmark(ABC):
    """Base class for reproducible reasoning benchmarks."""
    name: str = "base"
    domain: str = "general"
    difficulty: float = 0.5
    seed: int | None = None

    def __init__(self, seed: int | None = None):
        self.seed = seed or random.randint(1, 100000)
        self.rng = random.Random(self.seed)

    @abstractmethod
    def generate_task(self) -> Dict[str, Any]:
        """Generate a task instance."""
        pass

    @abstractmethod
    def score(self, agent_output: Dict[str, Any]) -> float:
        """Score agent output against expected criteria."""
        pass

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "domain": self.domain,
            "difficulty": self.difficulty,
            "seed": self.seed
        }