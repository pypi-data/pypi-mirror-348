import json
import time
from typing import Any, Dict


class StreamHandler:
    def __init__(self):
        self.buffer = ""
        self.generated_text = ""
        self.first_token_time = None
        self.response_format = None
        self.special_tokens = {
            "start_header": "<|start_header_id|>",
            "end_header": "<|end_header_id|>",
            "eot": "<|eot_id|>",
        }

    def process_chunk(self, chunk: str) -> str:
        if not self.response_format == "openai":
            self.detect_format(chunk)

        if self.response_format == "openai":
            return self.process_openai_chunk(chunk)
        elif self.response_format == "special_tokens":
            return self.process_special_tokens_chunk(chunk)
        else:
            return chunk

    def process_special_tokens_chunk(self, chunk: str) -> str:
        # Remove the header if present
        if (
            self.special_tokens["start_header"] in chunk
            and self.special_tokens["end_header"] in chunk
        ):
            _, chunk = chunk.split(self.special_tokens["end_header"], 1)
            chunk = chunk.lstrip()  # Remove leading whitespace
            if not chunk:  # If chunk is empty after removing header, return empty string
                return ""

        # Remove the EOT token if present
        if self.special_tokens["eot"] in chunk:
            chunk, _ = chunk.split(self.special_tokens["eot"], 1)

        return chunk

    def process_openai_chunk(self, chunk: str) -> str:
        chunk = chunk.strip()

        if chunk.startswith("data: "):
            chunk = chunk[6:]
        # Remove 'data: ' prefix
        if chunk == "[DONE]":
            return ""
        if chunk == "":
            return ""
        try:
            data = json.loads(chunk)
            if len(data["choices"]) == 0:
                return ""
            return data["choices"][0]["delta"].get("content", "")
        except json.JSONDecodeError:
            return ""

    def detect_format(self, chunk: str):
        if chunk.startswith("data: "):
            self.response_format = "openai"
        elif any(token in chunk for token in self.special_tokens.values()):
            self.response_format = "special_tokens"
        else:
            self.response_format = "unknown"

    def update_metrics(self, content: str):
        if content and self.first_token_time is None:
            self.first_token_time = time.perf_counter()
        if content is not None:
            self.generated_text += content

    def get_results(self) -> Dict[str, Any]:
        return {"generated_text": self.generated_text, "first_token_time": self.first_token_time}
