import json
from typing import Dict, List
from pathlib import Path

class MuseumOfMinds:
    """Archive of evolved genomes, notable runs, and emergent behaviors."""

    def __init__(self, base_dir: str = "museum"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)

    def archive_run(self, world_id: str, generation: int, best_genome, artifacts: Dict):
        run_data = {
            "world_id": world_id,
            "generation": generation,
            "genome_id": best_genome.id,
            "artifacts": artifacts,
            "notable_traits": self._extract_notable(best_genome)
        }
        path = self.base_dir / f"mind_{world_id}_{generation}.json"
        with open(path, "w") as f:
            json.dump(run_data, f, indent=2)

    def _extract_notable(self, genome):
        return {
            "creativity": genome.creativity_bias,
            "skepticism": genome.skepticism,
            "reasoning_style": genome.reasoning_style
        }