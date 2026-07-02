import json
from difflib import SequenceMatcher
from typing import Dict, Any, Tuple
from world_loop.llm.provider import LLMProvider

class HybridEvaluator:
    def __init__(self, llm: LLMProvider):
        self.llm = llm

    async def score_async(self, artifacts: Dict[str, Any], world, history: Dict[str, Any]) -> Tuple[float, Dict[str, float]]:
        breakdown = {}
        combined_text = str(artifacts).lower()
        
        # Deterministic Match
        breakdown["constraint_match"] = 0.0
        if world.constraints:
            for constraint in world.constraints:
                if constraint.lower()[:15] in combined_text:
                    breakdown["constraint_match"] += (1.0 / len(world.constraints))
        else:
            breakdown["constraint_match"] = 1.0
            
        # Novelty
        novelty_score = 1.0
        if history:
            all_past = [str(run.get("artifacts")) for run in history.values()]
            similarities = [SequenceMatcher(None, combined_text, past).ratio() for past in all_past]
            if similarities:
                novelty_score = 1.0 - max(similarities)
        breakdown["novelty"] = novelty_score

        # LLM Judge
        llm_score = await self._llm_judge(artifacts, world)
        breakdown["llm_semantic_score"] = llm_score

        alpha, beta, gamma = 0.5, 0.3, 0.2
        final_score = (alpha * llm_score) + (beta * breakdown["constraint_match"]) + (gamma * novelty_score)
        
        return min(max(final_score, 0.0), 1.0), breakdown

    async def _llm_judge(self, artifacts: Dict[str, Any], world) -> float:
        system_prompt = (
            "You are an impartial judge. Evaluate the provided agent output against the World Goal. "
            "Output ONLY a JSON object with a single key 'score' containing a float between 0.0 and 1.0."
        )
        user_prompt = (
            f"Goal: {world.goal}\n"
            f"Constraints: {world.constraints}\n"
            f"Agent Output: {json.dumps(artifacts)}\n\n"
            "Evaluate logical soundness and constraint adherence."
        )
        try:
            response = await self.llm.generate(user_prompt, system_prompt, temperature=0.0)
            data = json.loads(response)
            return float(data.get("score", 0.0))
        except Exception:
            return 0.0