import time
from typing import Any, Dict, Optional

import aiohttp
from transformers import AutoTokenizer

from baseten_benchmarks.llm_provider import LLMProvider
from baseten_benchmarks.request_types import RequestResult
from baseten_benchmarks.stream_handler import StreamHandler


class GenericRestProvider(LLMProvider):
    def __init__(self, args):
        self.api_url = args.api_url
        self.api_key = args.api_key
        self.tokenizer = self._init_tokenizer(args.tokenizer)
        self.args = args
        self.prompt_style = args.prompt_style
        self.model_name = args.model

    def _init_tokenizer(self, tokenizer_name: Optional[str]):
        if tokenizer_name:
            return AutoTokenizer.from_pretrained(tokenizer_name)
        return None

    def _tokenize(self, text: str) -> list:
        if self.tokenizer:
            return self.tokenizer.encode(text)
        return text.split()  # Simple fallback tokenization

    async def generate(self, prompt: str, session) -> "RequestResult":
        payload = self._prepare_payload(prompt, self.args.stream)
        headers = self._prepare_headers()

        start_time = time.perf_counter()
        if self.args.stream:
            return await self._handle_streaming_response(
                payload=payload,
                headers=headers,
                start_time=start_time,
                prompt=prompt,
                session=session,
            )
        else:
            return await self._handle_non_streaming_response(
                payload=payload,
                headers=headers,
                start_time=start_time,
                prompt=prompt,
                session=session,
            )

    def _prepare_payload(self, prompt: str, stream: bool) -> Dict[str, Any]:
        payload = {
            "stream": stream,
            "max_tokens": self.args.output_len,
            "ignore_eos": True,
            **self.args.extra_request_body,
        }
        if self.prompt_style == "messages":
            payload["messages"] = [{"role": "user", "content": prompt}]
        else:
            payload["prompt"] = prompt

        if self.model_name:
            payload["model"] = self.model_name

        if self.args.stream:
            payload["stream"] = self.args.stream

        return {k: v for k, v in payload.items() if v is not None}

    def _prepare_headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json", "Authorization": f"Api-Key {self.api_key}"}

    async def _handle_non_streaming_response(
        self,
        payload: Dict[str, Any],
        headers: Dict[str, str],
        start_time: float,
        prompt: str,
        session: aiohttp.ClientSession,
    ) -> "RequestResult":
        async with session.post(
            self.api_url, json=payload, headers=headers, timeout=None
        ) as response:
            end_time = time.perf_counter()
            response_text = await response.text()
            return RequestResult(
                success=True,
                generated_text=response_text,
                latency=end_time - start_time,
                ttft=0,
                prompt=prompt,
            )

    async def _handle_streaming_response(
        self,
        payload: Dict[str, Any],
        headers: Dict[str, str],
        start_time: float,
        prompt: str,
        session: aiohttp.ClientSession,
    ) -> "RequestResult":
        time.perf_counter()
        response = await session.post(self.api_url, json=payload, headers=headers, timeout=None)
        # logger.info(f"Streaming request sent at {request_sent_time - START_TIME:.6f} seconds after TEST start")

        async with response:
            if response.status != 200:
                return RequestResult(
                    success=False,
                    error=f"API Error: HTTP {response.status}",
                    latency=0,
                    ttft=0,
                    prompt=prompt,
                )

            stream_handler = StreamHandler()

            async for chunk in response.content:
                # print(chunk)
                chunk = chunk.decode("utf-8")
                content = stream_handler.process_chunk(chunk)
                stream_handler.update_metrics(content)

            end_time = time.perf_counter()
            results = stream_handler.get_results()
            latency = end_time - start_time
            ttft = results["first_token_time"] - start_time if results["first_token_time"] else 0

            return RequestResult(
                success=True,
                generated_text=results["generated_text"],
                latency=latency,
                ttft=ttft,
                prompt=prompt,
            )

    def _extract_generated_text(self, json_response: Dict[str, Any]) -> str:
        return json_response.get("generated_text", "")


def get_llm_provider(args) -> LLMProvider:
    if args.backend == "generic":
        return GenericRestProvider(args)
    else:
        raise ValueError(f"Unsupported backend: {args.backend}")
