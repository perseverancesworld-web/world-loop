from ..base import Benchmark
from ..registry import register_benchmark
import random

@register_benchmark("arithmetic")
class ArithmeticBenchmark(Benchmark):
    name = "arithmetic"
    domain = "mathematics"

    def generate_task(self) -> dict:
        a = self.rng.randint(10, 999)
        b = self.rng.randint(10, 999)
        return {
            "problem": f"What is {a} + {b}?",
            "answer": a + b,
            "type": "addition"
        }

    def score(self, agent_output: dict) -> float:
        try:
            provided = int(agent_output.get("answer", 0))
            expected = self.generate_task()["answer"]
            return 1.0 if provided == expected else 0.0
        except:
            return 0.0