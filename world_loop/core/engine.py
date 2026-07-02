import asyncio, uuid, time
from typing import Dict, Any
from world_loop.core.seed import SeedWorld
from world_loop.population import Population
from world_loop.agents.roles import Planner, Builder, Critic, Verifier

class AsyncEngine:
    def __init__(self, llm_provider, evaluator, memory, seed_engine, mutator=None):
        from world_loop.mutate.mutator import Mutator
        self.llm = llm_provider
        self.evaluator = evaluator
        self.memory = memory
        self.seed_engine = seed_engine
        self.mutator = mutator or Mutator()

    async def run_epoch_async(self, world: SeedWorld, population: Population) -> Dict[str, Any]:
        history = self.memory.get_history(world.id)
        
        tasks = [
            self._run_agent_cycle_async(world, genome, history)
            for genome in population.genomes
        ]
        
        cycle_results = await asyncio.gather(*tasks)
        
        results = []
        for pop_genome, res in zip(population.genomes, cycle_results):
            results.append((pop_genome, res["artifacts"], res["score"]))
            # Persist to memory
            run_id = str(uuid.uuid4())
            self.memory.save_run(world.id, run_id, {
                "genome_id": pop_genome.id,
                "artifacts": res["artifacts"],
                "score": res["score"]
            })
        
        best_genome, best_artifact, best_score = max(results, key=lambda x: x[2])
        
        if best_score > 0.85:
            world = self.mutator.mutate_world(world, best_score)
        
        population.evolve(results, mutation_rate=world.mutation_rate)
        
        return {
            "best_score": best_score,
            "best_genome_id": best_genome.id,
            "world_difficulty": world.difficulty,
            "token_usage": self.llm.usage
        }

    async def _run_agent_cycle_async(self, world, genome, history):
        planner = Planner(world, genome, self.llm)
        builder = Builder(world, genome, self.llm)
        critic = Critic(world, genome, self.llm)
        verifier = Verifier(world, genome, self.llm)
        
        plan = await planner.act()
        build = await builder.act(plan)
        critique = await critic.act(build)
        verification = await verifier.act(build, critique)
        
        artifacts = {
            "planner": plan,
            "builder": build,
            "critic": critique,
            "verifier": verification
        }
        
        score, breakdown = await self.evaluator.score_async(artifacts, world, history)
        return {"artifacts": artifacts, "score": score, "breakdown": breakdown}