from ..base import Benchmark
from ..registry import register_benchmark

@register_benchmark("mars_habitat")
class MarsHabitatBenchmark(Benchmark):
    name = "mars_habitat"
    domain = "systems_architecture"
    difficulty = 0.6

    def generate_task(self) -> dict:
        return {
            "goal": "Design a basic closed-loop life support system for 4 people on Mars.",
            "constraints": ["Power < 100kW", "Water recycling > 80%", "Radiation protection"],
            "expected": ["redundancy", "regolith use", "power management"]
        }

    def score(self, agent_output: dict) -> float:
        # Simple keyword + structure score
        text = str(agent_output).lower()
        score = 0.0
        for kw in ["power", "water", "radiation", "redundancy"]:
            if kw in text:
                score += 0.25
        return min(score, 1.0)