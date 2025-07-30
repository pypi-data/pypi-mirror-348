import asyncio
import logging
import time
from typing import List

import aiohttp
from tqdm import tqdm
from transformers import AutoTokenizer

from baseten_benchmarks import parse_args
from baseten_benchmarks.input_handler import InputHandler
from baseten_benchmarks.llm_provider import LLMProvider
from baseten_benchmarks.request_types import RequestResult


logger = logging.getLogger(__name__)


class RequestHandler:
    def __init__(self, provider: LLMProvider, args: parse_args.AppConfig):
        self.provider = provider
        # Default to the first concurrency
        self.concurrency = args.concurrency[0]
        self.request_rate = args.request_rate
        self.tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)

        # set timeout to 20 minutes
        self.timeout = 1200
        self.stream = args.stream
        self.disable_tqdm = args.disable_tqdm
        self.warmup_results = []
        self.initial_delay = 0.01
        self.input_handler = InputHandler(args)

    async def warmup(self, prompts, num_warmup_requests: int = 5):
        logger.info("Performing warmup requests...")
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=32, keepalive_timeout=30),
            timeout=aiohttp.ClientTimeout(total=6 * 60 * 60, connect=60, sock_connect=60),
        ) as session:
            warmup_tasks = [
                self.provider.generate(prompt, session) for prompt in prompts[:num_warmup_requests]
            ]
            self.warmup_results = await asyncio.gather(*warmup_tasks)
        logger.info("Warmup completed.")
        # This is too conservative, setting it to 0.01 manually yields better results
        # self._calculate_initial_delay()

    def _calculate_initial_delay(self):
        if self.warmup_results:
            delays = [
                r.ttft - ((r.latency - r.ttft) / len(self.tokenizer.encode(r.generated_text)))
                for r in self.warmup_results
                if r.success
            ]
            if delays:
                self.initial_delay = sum(delays) / len(delays)
        logger.info(f"Initial delay set to {self.initial_delay:.3f} seconds")

    async def make_request(self, prompt: str, session: aiohttp.ClientSession) -> RequestResult:
        start_time = time.perf_counter()
        result = await asyncio.wait_for(
            self.provider.generate(prompt, session), timeout=self.timeout
        )
        end_time = time.perf_counter()
        result.latency = end_time - start_time
        return result

    async def run_benchmark(self, prompts: List[str]) -> List[RequestResult]:
        if self.request_rate < float("inf") and self.concurrency == float("inf"):
            return await self.run_rate_only_benchmark(prompts)
        elif self.request_rate < float("inf"):
            return await self.run_rate_limited_benchmark(prompts)
        else:
            return await self.run_max_concurrency_benchmark(prompts)

    async def run_timed_benchmark(self, duration: int) -> List[RequestResult]:
        results = []
        end_time = time.perf_counter() + duration
        prompts = self.input_handler.get_timed_prompts()
        concurrency = int(self.concurrency)
        semaphore = asyncio.Semaphore(concurrency)

        async def controlled_request():
            async with semaphore:
                prompt = next(prompts)
                return await self.make_request(prompt)

        with tqdm(total=duration, disable=self.disable_tqdm, unit="s") as pbar:
            while time.perf_counter() < end_time:
                if self.request_rate < float("inf"):
                    await asyncio.sleep(1 / self.request_rate)

                task = asyncio.create_task(controlled_request())
                result = await task
                results.append(result)
                pbar.update(
                    min(time.perf_counter() - pbar.last_print_t, end_time - time.perf_counter())
                )

                if not result.success:
                    logger.error(f"Error: {result.error}")

        return results

    async def run_rate_limited_benchmark(self, prompts: List[str]) -> List[RequestResult]:
        logger.info(
            f"Running rate limited benchmark with concurrency {self.concurrency} and request rate {self.request_rate}"
        )
        results = []
        concurrency = int(self.concurrency)
        semaphore = asyncio.Semaphore(concurrency)
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=32, keepalive_timeout=30),
            timeout=aiohttp.ClientTimeout(total=6 * 60 * 60, connect=60, sock_connect=60),
        ) as session:

            async def controlled_request(prompt):
                async with semaphore:
                    return await self.make_request(prompt, session)

            tasks = []

            # Create tasks with appropriate delays
            for i, prompt in enumerate(prompts):
                await asyncio.sleep(1 / self.request_rate)  # Delay before creating each task
                tasks.append(asyncio.create_task(controlled_request(prompt)))

            with tqdm(total=len(prompts), disable=self.disable_tqdm) as pbar:
                for task in asyncio.as_completed(tasks):
                    result = await task
                    results.append(result)
                    pbar.update(1)
                    if not result.success:
                        logger.error(f"Error: {result.error}")

            return results

    async def run_max_concurrency_benchmark(self, prompts: List[str]) -> List[RequestResult]:
        results = []
        concurrency = int(self.concurrency)
        semaphore = asyncio.Semaphore(concurrency)
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=32, keepalive_timeout=30),
            timeout=aiohttp.ClientTimeout(total=6 * 60 * 60, connect=60, sock_connect=60),
        ) as session:

            async def controlled_request(prompt):
                async with semaphore:
                    return await self.make_request(prompt, session)

            tasks = []

            # Stagger only the initial batch (up to concurrency limit)
            for i, prompt in enumerate(prompts[: self.concurrency]):
                await asyncio.sleep(
                    i * self.initial_delay
                )  # Delay before starting each request in the initial batch
                tasks.append(asyncio.create_task(controlled_request(prompt)))

            # Queue the remaining prompts to run immediately as spots open up in the semaphore
            for prompt in prompts[self.concurrency :]:
                tasks.append(asyncio.create_task(controlled_request(prompt)))

            with tqdm(total=len(prompts), disable=self.disable_tqdm) as pbar:
                for task in asyncio.as_completed(tasks):
                    result = await task
                    results.append(result)
                    pbar.update(1)
                    if not result.success:
                        logger.error(f"Error: {result.error}")

        return results

    async def run_rate_only_benchmark(self, prompts: List[str]) -> List[RequestResult]:
        results = []
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=32, keepalive_timeout=30),
            timeout=aiohttp.ClientTimeout(total=6 * 60 * 60, connect=60, sock_connect=60),
        ) as session:

            async def controlled_request(prompt):
                return await self.make_request(prompt, session)

            tasks = []

            # Create tasks with appropriate delays
            for i, prompt in enumerate(prompts):
                await asyncio.sleep(1 / self.request_rate)  # Delay before creating each task
                tasks.append(asyncio.create_task(controlled_request(prompt)))

            with tqdm(total=len(prompts), disable=self.disable_tqdm) as pbar:
                for task in asyncio.as_completed(tasks):
                    result = await task
                    results.append(result)
                    pbar.update(1)
                    if not result.success:
                        logger.error(f"Error: {result.error}")

        return results
