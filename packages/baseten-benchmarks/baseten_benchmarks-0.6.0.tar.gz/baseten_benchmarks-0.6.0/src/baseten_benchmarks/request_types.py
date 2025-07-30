from dataclasses import dataclass
from typing import Optional


@dataclass
class RequestResult:
    success: bool
    latency: float
    ttft: float
    error: Optional[str] = None
    generated_text: Optional[str] = None
    prompt: Optional[str] = None


@dataclass
class RequestMetrics:
    success: bool
    latency: float
    ttft: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    tokens_per_second: float
    tpot: float
    error: Optional[str] = None
    generated_text: Optional[str] = None
    prompt: Optional[str] = None
