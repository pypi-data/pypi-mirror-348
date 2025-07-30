from typing import Any, Dict, List

from transformers import AutoTokenizer

from baseten_benchmarks.request_types import RequestMetrics, RequestResult


class MetricsCalculator:
    def __init__(self, tokenizer_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    def calculate_request_metrics(self, result: RequestResult) -> RequestMetrics:
        prompt_token_count = len(self.tokenizer.encode(result.prompt))
        completion_token_count = (
            len(self.tokenizer.encode(result.generated_text)) if result.generated_text else 0
        )
        total_tokens = prompt_token_count + completion_token_count

        tokens_per_second = total_tokens / result.latency if result.latency > 0 else 0

        # Calculate TPOT
        tpot = 0
        if completion_token_count > 0:
            tpot = (result.latency - result.ttft) / completion_token_count

        return RequestMetrics(
            success=result.success,
            latency=result.latency,
            ttft=result.ttft,
            prompt_tokens=prompt_token_count,
            completion_tokens=completion_token_count,
            total_tokens=total_tokens,
            tokens_per_second=tokens_per_second,
            tpot=tpot,
            error=result.error,
            generated_text=result.generated_text,
            prompt=result.prompt,
        )

    def calculate_aggregate_metrics(
        self, request_metrics: List[RequestMetrics], concurrency: int, test_times: Dict[int, float]
    ) -> Dict[str, Any]:
        successful_requests = [r for r in request_metrics if r.success]

        if not successful_requests:
            return self._empty_metrics(len(request_metrics))

        metrics = {
            "total_requests": len(request_metrics),
            "successful_requests": len(successful_requests),
            "failure_rate": 1 - (len(successful_requests) / len(request_metrics)),
        }

        latencies = [r.latency for r in successful_requests]
        ttfts = [r.ttft for r in successful_requests]
        prompt_tokens = [r.prompt_tokens for r in successful_requests]
        completion_tokens = [r.completion_tokens for r in successful_requests]
        total_tokens = [r.total_tokens for r in successful_requests]
        tpots = [r.tpot for r in successful_requests]

        metrics.update(
            {
                "average_latency": sum(latencies) / len(latencies),
                "p50_latency": sorted(latencies)[len(latencies) // 2],
                "p90_latency": sorted(latencies)[int(len(latencies) * 0.9)],
                "p99_latency": sorted(latencies)[int(len(latencies) * 0.99)],
                "average_ttft": sum(ttfts) / len(ttfts),
                "p50_ttft": sorted(ttfts)[len(ttfts) // 2],
                "p90_ttft": sorted(ttfts)[int(len(ttfts) * 0.9)],
                "p99_ttft": sorted(ttfts)[int(len(ttfts) * 0.99)],
                "average_tpot": sum(tpots) / len(tpots),
                "p50_tpot": sorted(tpots)[len(tpots) // 2],
                "p90_tpot": sorted(tpots)[int(len(tpots) * 0.9)],
                "p99_tpot": sorted(tpots)[int(len(tpots) * 0.99)],
                "average_prompt_tokens": sum(prompt_tokens) / len(prompt_tokens),
                "average_completion_tokens": sum(completion_tokens) / len(completion_tokens),
                "average_total_tokens": sum(total_tokens) / len(total_tokens),
                "total_prompt_tokens": sum(prompt_tokens),
                "total_completion_tokens": sum(completion_tokens),
                "total_tokens": sum(total_tokens),
                "average_perceived_tokens_per_second": sum(completion_tokens) / sum(latencies),
            }
        )

        metrics["average_overall_throughput"] = (
            metrics["average_perceived_tokens_per_second"] * concurrency
        )

        return metrics

    def _empty_metrics(self, total_requests: int) -> Dict[str, Any]:
        return {
            "total_requests": total_requests,
            "successful_requests": 0,
            "failure_rate": 1.0,
            "average_latency": 0,
            "p50_latency": 0,
            "p90_latency": 0,
            "p99_latency": 0,
            "average_ttft": 0,
            "p50_ttft": 0,
            "p90_ttft": 0,
            "p99_ttft": 0,
            "average_prompt_tokens": 0,
            "average_completion_tokens": 0,
            "average_total_tokens": 0,
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_tokens": 0,
            "average_perceived_tokens_per_second": 0,
            "average_overall_throughput": 0,
            "average_tpot": 0,
            "p50_tpot": 0,
            "p90_tpot": 0,
            "p99_tpot": 0,
        }
