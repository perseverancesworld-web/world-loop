from world_loop.agents.base import AsyncBaseAgent

class Planner(AsyncBaseAgent):
    async def act(self) -> dict:
        return await self.execute(
            role="planner",
            context="Initial phase.",
            instruction="Analyze the goal, extract core problems, and output a JSON with 'plan' and 'steps' (list)."
        )

class Builder(AsyncBaseAgent):
    async def act(self, plan: dict) -> dict:
        return await self.execute(
            role="builder",
            context=f"Plan provided: {plan}",
            instruction="Draft a full solution following the plan. Output a JSON with 'design' and 'components'."
        )

class Critic(AsyncBaseAgent):
    async def act(self, build: dict) -> dict:
        intensity = "Harshly" if self.genome.skepticism > 0.5 else "Gently"
        return await self.execute(
            role="critic",
            context=f"Proposed Build: {build}",
            instruction=f"{intensity} find flaws and constraint violations. Output JSON with 'flaws' (list)."
        )

class Verifier(AsyncBaseAgent):
    async def act(self, build: dict, critique: dict) -> dict:
        return await self.execute(
            role="verifier",
            context=f"Build: {build}\nCritique: {critique}",
            instruction="Check if the build survives the critique. Output JSON with 'status' (pass/fail) and 'reason'."
        )