import asyncio
import logging
import random
import sys

from baseten_benchmarks import parse_args
from baseten_benchmarks.benchmark_executor import BenchmarkExecutor


logger: logging.Logger | None = None


async def main(args: parse_args.AppConfig):
    random.seed(args.random_seed)
    executor = BenchmarkExecutor(args)
    output = await executor.execute()

    if logger is not None:
        logger.info(output)
        logger.info(f"Detailed results saved to {args.model}/{args.output_file}")


def run():
    args = parse_args.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    global logger
    logger = logging.getLogger(__name__)
    asyncio.run(main(args))


if __name__ == "__main__":
    run()
