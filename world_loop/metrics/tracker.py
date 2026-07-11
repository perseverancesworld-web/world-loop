from typing import Dict, List
import json

class EvolutionMetrics:
    """Tracks genome drift, specialization, convergence."""

    def __init__(self):
        self.history = []

    def log_generation(self, generation: int, population_data: List[Dict]):
        self.history.append({
            "generation": generation,
            "avg_fitness": sum(d.get("score", 0) for d in population_data) / len(population_data),
            "trait_variance": self._compute_variance(population_data)
        })

    def _compute_variance(self, data):
        # Placeholder for trait variance
        return 0.15  # to be expanded

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self.history, f, indent=2)