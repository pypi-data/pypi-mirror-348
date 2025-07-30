from abc import ABC, abstractmethod

import aiohttp

from baseten_benchmarks.request_types import RequestResult


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, session: aiohttp.ClientSession) -> RequestResult:
        pass
