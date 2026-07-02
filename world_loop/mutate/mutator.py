import random
from world_loop.genome import CognitiveGenome
from world_loop.core.seed import SeedWorld
import uuid

class Mutator:
    def __init__(self, rng: random.Random = None):
        self.rng = rng or random.Random()

    def jitter(self, v: float, intensity: float) -> float:
        delta = self.rng.uniform(-intensity, intensity)
        return max(0.0, min(1.0, v + delta))

    def mutate(self, genome: CognitiveGenome, intensity: float = 0.1) -> CognitiveGenome:
        g = genome.copy()
        g.id = str(uuid.uuid4())
        g.parent_id = genome.id
        g.generation = genome.generation + 1
        
        g.exploration_rate = self.jitter(g.exploration_rate, intensity)
        g.constraint_tolerance = self.jitter(g.constraint_tolerance, intensity)
        g.hallucination_rate = self.jitter(g.hallucination_rate, intensity)
        g.verbosity = self.jitter(g.verbosity, intensity)
        g.skepticism = self.jitter(g.skepticism, intensity)
        g.creativity_bias = self.jitter(g.creativity_bias, intensity)
        
        if self.rng.random() < intensity * 0.5:
            g.reasoning_style = self.rng.choice(["analytical", "synthetic", "intuitive", "adversarial"])
            
        return g

    def mutate_world(self, world: SeedWorld, score: float) -> SeedWorld:
        if score > 0.85:
            world.difficulty = min(world.difficulty + world.mutation_rate, 1.0)
            if self.rng.random() < world.noise:
                world.constraints.append("Optimize for extreme redundancy.")
        return world