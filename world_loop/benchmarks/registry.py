from typing import Dict, Type
from .base import Benchmark

BENCHMARK_REGISTRY: Dict[str, Type[Benchmark]] = {}

def register_benchmark(name: str):
    def decorator(cls: Type[Benchmark]):
        BENCHMARK_REGISTRY[name] = cls
        return cls
    return decorator

def get_benchmark(name: str, seed: int | None = None) -> Benchmark:
    if name not in BENCHMARK_REGISTRY:
        raise ValueError(f"Benchmark {name} not registered")
    return BENCHMARK_REGISTRY[name](seed=seed)