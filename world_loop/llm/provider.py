import os, json, aiohttp

class LLMProvider:
    def __init__(self, backend: str = "ollama", model: str = "llama3"):
        self.backend = backend
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY") if backend == "openai" else None
        self.usage = {"prompt_tokens": 0, "completion_tokens": 0}

    async def generate(self, prompt: str, system: str, temperature: float = 0.7) -> str:
        if self.backend == "ollama":
            return await self._call_ollama(prompt, system, temperature)
        elif self.backend == "openai":
            return await self._call_openai(prompt, system, temperature)
        else:
            raise ValueError(f"Unsupported backend: {self.backend}")

    async def _call_ollama(self, prompt: str, system: str, temp: float) -> str:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": self.model,
            "system": system,
            "prompt": prompt,
            "temperature": temp,
            "stream": False,
            "format": "json"
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        self.usage["completion_tokens"] += data.get("eval_count", 0)
                        return data.get("response", "")
                    return '{"error": "Local LLM failed"}'
            except Exception as e:
                return f'{{"error": "Connection failed: {str(e)}" }}'

    async def _call_openai(self, prompt: str, system: str, temp: float) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        payload = {
            "model": self.model,
            "temperature": temp,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        usage = data.get("usage", {})
                        self.usage["prompt_tokens"] += usage.get("prompt_tokens", 0)
                        self.usage["completion_tokens"] += usage.get("completion_tokens", 0)
                        return data["choices"][0]["message"]["content"]
                    return '{"error": "Cloud LLM failed"}'
            except Exception as e:
                return f'{{"error": "Connection failed: {str(e)}" }}'