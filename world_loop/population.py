import random
from typing import List, Tuple
from world_loop.genome import CognitiveGenome
from world_loop.mutate.mutator import Mutator

class Population:
    def __init__(self, size: int = 4, rng_seed: int | None = None):
        self.size = size
        self.rng = random.Random(rng_seed)
        self.genomes: List[CognitiveGenome] = [self._spawn() for _ in range(size)]
        self.mutator = Mutator(self.rng)

    def _spawn(self) -> CognitiveGenome:
        return CognitiveGenome(
            exploration_rate=self.rng.random(),
            skepticism=self.rng.random(),
            creativity_bias=self.rng.random()
        )

    def evolve(self, scored: List[Tuple[CognitiveGenome, dict, float]], mutation_rate: float = 0.1):
        scored_sorted = sorted(scored, key=lambda x: x[2], reverse=True)
        top_count = max(1, self.size // 4)
        survivors = [g for g, a, s in scored_sorted[:top_count]]
        
        new_genomes = survivors[:]
        while len(new_genomes) < self.size:
            parent = self.rng.choice(survivors)
            child = self.mutator.mutate(parent, mutation_rate)
            new_genomes.append(child)
            
        self.genomes = new_genomes