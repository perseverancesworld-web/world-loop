import json
from world_loop.llm.provider import LLMProvider

class AsyncBaseAgent:
    def __init__(self, world, genome, llm: LLMProvider):
        self.world = world
        self.genome = genome
        self.llm = llm

    async def execute(self, role: str, context: str, instruction: str) -> dict:
        temperature = 0.1 + (self.genome.creativity_bias * 0.8) 
        verbosity = "highly detailed" if self.genome.verbosity > 0.5 else "extremely concise"
        
        system_prompt = (
            f"You are a {role} in an AI system. "
            f"Your reasoning style is {self.genome.reasoning_style}. "
            f"Be {verbosity}. Output strictly in valid JSON format."
        )

        user_prompt = (
            f"World Goal: {self.world.goal}\n"
            f"Constraints: {self.world.constraints}\n"
            f"Context: {context}\n\n"
            f"Task: {instruction}\n"
            f"Respond only with a JSON object."
        )

        raw_response = await self.llm.generate(user_prompt, system_prompt, temperature)
        try:
            return json.loads(raw_response)
        except json.JSONDecodeError:
            return {"role": role, "error": "JSON parse failed", "raw": raw_response}