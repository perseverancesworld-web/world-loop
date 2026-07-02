import argparse, json, os, time, asyncio
from world_loop.core.seed import SeedEngine
from world_loop.core.engine import AsyncEngine
from world_loop.population import Population
from world_loop.eval.evaluator import HybridEvaluator
from world_loop.llm.provider import LLMProvider
from world_loop.memory.inmemory import InMemoryStore

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

async def main_async():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", required=True)
    p.add_argument("--epochs", type=int, default=5)
    p.add_argument("--pop", type=int, default=4)
    p.add_argument("--out", default="runs")
    p.add_argument("--provider", choices=["ollama", "openai"], default="ollama")
    p.add_argument("--model", default="llama3")
    args = p.parse_args()

    with open(args.seed, "r") as f:
        seed_spec = json.load(f)

    llm = LLMProvider(backend=args.provider, model=args.model)
    evaluator = HybridEvaluator(llm=llm)
    seed_engine = SeedEngine()
    memory = InMemoryStore()
    
    engine = AsyncEngine(llm_provider=llm, evaluator=evaluator, memory=memory, seed_engine=seed_engine)
    
    world = seed_engine.generate(seed_spec["domain"], seed_spec["goal"], seed_spec)
    population = Population(size=args.pop)
    
    ensure_dir(args.out)
    world_dir = os.path.join(args.out, world.id)
    ensure_dir(world_dir)

    print(f"🌍 World Generated: {world.id[:8]} | Pop: {args.pop} | LLM: {args.provider.upper()}")
    print("-" * 50)

    lineage = {"world_id": world.id, "epochs": []}

    for epoch in range(1, args.epochs + 1):
        start_time = time.time()
        result = await engine.run_epoch_async(world, population)
        elapsed = time.time() - start_time
        
        print(f"Epoch {epoch:02d} | Score: {result['best_score']:.3f} | Best ID: {result['best_genome_id'][:8]} | {elapsed:.1f}s")

        epoch_file = os.path.join(world_dir, f"epoch_{epoch:03d}.json")
        payload = {
            "epoch": epoch,
            "best_score": result["best_score"],
            "world_difficulty": result["world_difficulty"],
            "best_genome_id": result["best_genome_id"],
        }
        with open(epoch_file, "w") as f:
            json.dump(payload, f, indent=2)
        lineage["epochs"].append(payload)

    lineage["final_usage"] = result.get("token_usage", {})
    with open(os.path.join(world_dir, "lineage.json"), "w") as f:
        json.dump(lineage, f, indent=2)
        
    print("-" * 50)
    print(f"✅ Evolution Complete. Tokens: {lineage['final_usage']}")

def main():
    asyncio.run(main_async())

if __name__ == "__main__":
    main()