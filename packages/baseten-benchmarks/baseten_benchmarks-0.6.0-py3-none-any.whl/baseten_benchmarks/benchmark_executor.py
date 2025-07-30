import csv
import logging
import os
import time
from dataclasses import asdict
from typing import Any, Dict, List

from baseten_benchmarks import parse_args
from baseten_benchmarks.generic_rest_provider import get_llm_provider
from baseten_benchmarks.input_handler import InputHandler
from baseten_benchmarks.metrics_calculator import MetricsCalculator
from baseten_benchmarks.request_handler import RequestHandler
from baseten_benchmarks.request_types import RequestResult


logger = logging.getLogger(__name__)


class BenchmarkExecutor:
    def __init__(self, args: parse_args.AppConfig):
        self.args = args
        self.metrics_calculator = MetricsCalculator(args.tokenizer)
        self.warmup_run_counter = 0
        self.test_times = {}

    async def run(self) -> Dict[int, List[RequestResult]]:
        if self.args.duration is not None:
            return await self.run_timed_test(self.args.duration)
        else:
            return await self.run_standard_test()

    async def run_standard_test(self) -> Dict[int, List[RequestResult]]:
        all_results = {}

        for i, concurrency in enumerate(self.args.concurrency):
            start_time = time.perf_counter()
            logger.info(f"Running benchmark with concurrency: {concurrency}")

            # Create a new input handler with the appropriate prompt count index
            input_handler = InputHandler(self.args, prompt_count_index=i)
            prompts = input_handler.get_prompts()

            logger.info(f"Using {input_handler.prompt_count} prompts for concurrency {concurrency}")

            llm_provider = get_llm_provider(self.args)
            request_handler = RequestHandler(llm_provider, self.args)
            request_handler.concurrency = concurrency  # Set concurrency for this run
            request_handler.input_handler = input_handler  # Update input handler

            # Perform warmup
            if (
                not self.args.disable_warmup and self.warmup_run_counter < 1
            ):  # dont' run warmup for each concurrency
                warmup_prompts = input_handler.get_prompts()
                await request_handler.warmup(warmup_prompts, self.args.warmup_requests)
                self.warmup_run_counter += 1

            # Run the actual benchmark
            results = await request_handler.run_benchmark(prompts)
            all_results[concurrency] = results
            end_time = time.perf_counter()
            self.test_times[concurrency] = end_time - start_time

        return all_results

    async def run_timed_test(self, duration: int) -> Dict[int, List[RequestResult]]:
        concurrency = self.args.concurrency[0]  # We know there's only one value
        logger.info(
            f"\nRunning timed benchmark for {duration} seconds with concurrency {concurrency} and request rate {self.args.request_rate}"
        )

        # Create a new input handler with the appropriate prompt count index (0 for timed test)
        input_handler = InputHandler(self.args, prompt_count_index=0)
        logger.info(f"Using {input_handler.prompt_count} prompts for timed test")

        llm_provider = get_llm_provider(self.args)
        request_handler = RequestHandler(llm_provider, self.args)
        request_handler.concurrency = concurrency
        request_handler.input_handler = input_handler  # Update input handler

        # Perform warmup
        if not self.args.disable_warmup:
            warmup_prompts = input_handler.get_prompts()[: self.args.warmup_requests]
            await request_handler.warmup(warmup_prompts, self.args.warmup_requests)

        start_time = time.perf_counter()
        results = await request_handler.run_timed_benchmark(duration)
        end_time = time.perf_counter()

        self.test_times[concurrency] = end_time - start_time
        return {concurrency: results}

    def format_output(self, all_metrics: List[Dict[str, Any]]) -> str:
        output = "Benchmark Results:\n"
        for metrics in all_metrics:
            output += f"\nConcurrency: {metrics['concurrency']}, Request Rate: {metrics['request_rate']}\n"
            output += "-" * 50 + "\n"
            for key, value in metrics.items():
                if key not in ["concurrency", "request_rate"]:
                    if isinstance(value, float):
                        output += f"{key}: {value:.4f}\n"
                    else:
                        output += f"{key}: {value}\n"
        return output

    def save_results_to_csv(self, all_results: Dict[int, List[RequestResult]]):
        output_dir = os.path.join(os.getcwd(), self.args.model)
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, self.args.output_file)

        with open(output_file, "w", newline="") as csvfile:
            fieldnames = [
                "concurrency",
                "request_rate",
                "success",
                "latency",
                "ttft",
                "prompt_tokens",
                "completion_tokens",
                "total_tokens",
                "tokens_per_second",
                "tpot",
                "error",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for concurrency, results in all_results.items():
                for result in results:
                    metrics = self.metrics_calculator.calculate_request_metrics(result)
                    row = asdict(metrics)
                    row["concurrency"] = concurrency
                    row["request_rate"] = self.args.request_rate
                    # Remove prompt and generated_text from CSV output
                    row.pop("prompt", None)
                    row.pop("generated_text", None)
                    writer.writerow(row)

    def save_generated_text(self, all_results: Dict[int, List[RequestResult]]):
        output_dir = os.path.join(os.getcwd(), self.args.model)
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(
            output_dir, self.args.output_file.rsplit(".", 1)[0] + "_generated_text.txt"
        )
        with open(output_file, "w", encoding="utf-8") as f:
            for concurrency, results in all_results.items():
                f.write(f"Concurrency: {concurrency}\n")
                f.write("=" * 50 + "\n\n")
                for i, result in enumerate(results, 1):
                    f.write(f"Request {i}:\n")
                    if not self.args.no_prompt:
                        f.write(f"Prompt: {result.prompt}\n")
                    f.write(f"Generated Text: {result.generated_text}\n")
                    f.write("\n" + "-" * 50 + "\n\n")

    def calculate_final_metrics(
        self, all_results: Dict[int, List[RequestResult]]
    ) -> List[Dict[str, Any]]:
        all_metrics = []
        for concurrency, results in all_results.items():
            request_metrics = [
                self.metrics_calculator.calculate_request_metrics(r) for r in results
            ]
            metrics = self.metrics_calculator.calculate_aggregate_metrics(
                request_metrics, concurrency, self.test_times
            )
            metrics["concurrency"] = concurrency
            metrics["request_rate"] = self.args.request_rate
            all_metrics.append(metrics)
        return all_metrics

    async def execute(self) -> str:
        all_results = await self.run()
        self.save_results_to_csv(all_results)
        self.save_generated_text(all_results)
        aggregate_metrics = self.calculate_final_metrics(all_results)
        return self.format_output(aggregate_metrics)
