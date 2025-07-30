import logging
import random
import string
import sys
from pathlib import Path

from transformers import AutoTokenizer

from baseten_benchmarks import parse_args


logger = logging.getLogger(__name__)


class InputHandler:
    def __init__(self, args: parse_args.AppConfig, prompt_count_index=0):
        self.args = args
        # Use the specified prompt count index or default to the first one
        self.prompt_count = (
            args.num_prompts[prompt_count_index]
            if len(args.num_prompts) > 1
            else args.num_prompts[0]
        )

    def get_prompts(self):
        prompts = []
        if self.args.input_type == "random":
            prompts = self.generate_random_prompts()
        elif self.args.input_type == "file":
            prompts = self.read_prompts_from_file()
        elif self.args.input_type == "stdin":
            prompts = self.read_prompts_from_stdin()
        elif self.args.input_type == "custom":
            prompts = self.get_prompts_custom()
        else:
            raise ValueError(f"Invalid input type: {self.args.input_type}")

        return prompts * self.args.prompt_multiplier

    def get_timed_prompts(self):
        if self.args.input_type == "random":
            while True:
                yield self.generate_single_random_prompt()
        else:
            prompts = self.get_prompts()
            while True:
                yield from prompts

    def generate_single_random_prompt(self):
        return " ".join(
            "".join(random.choices(string.ascii_lowercase, k=5))
            for _ in range(self.args.random_input)
        )

    def get_prompts_custom(self):
        books_text_file = Path(__file__).parent / "data" / "books.txt"
        books_text = books_text_file.read_text(encoding="utf-8")

        # Initialize the tokenizer
        if self.args.tokenizer:
            tokenizer = AutoTokenizer.from_pretrained(self.args.tokenizer)
        else:
            logger.error("Tokenizer is required for custom input type")
            raise ValueError("Tokenizer is required for custom input type")

        # Create prompts by taking random subslices of the text
        prompts = []
        text_length = len(books_text)

        # Ensure the text is long enough to sample from
        if text_length < self.args.random_input * 10:
            logger.warning("Text file is relatively short for sampling, may get repetitive chunks")

        for _ in range(self.prompt_count):
            # Generate a random starting position
            if text_length > self.args.random_input * 5:
                # If the text is long enough, we can take truly random slices
                start_pos = random.randint(0, text_length - self.args.random_input * 5)
            else:
                # If text is short, use modulo to wrap around
                start_pos = random.randint(0, text_length - 1)

            # Extract a chunk that's larger than we need (to account for tokenization boundaries)
            text_chunk = books_text[start_pos : start_pos + self.args.random_input * 5]

            # Add a random token at the beginning to ensure uniqueness
            random_token = "".join(random.choices(string.ascii_lowercase, k=5))
            prompt_with_token = random_token + " " + text_chunk

            # Tokenize and truncate to random_input length
            tokenized_prompt = tokenizer(
                prompt_with_token,
                max_length=self.args.random_input,
                truncation=True,
                return_tensors="pt",
            ).input_ids

            # Convert token IDs back to text
            truncated_prompt = tokenizer.decode(tokenized_prompt[0], skip_special_tokens=True)
            prompts.append(truncated_prompt)

        return prompts

    def get_prompts_custom_old(self):
        try:
            with open("books.txt", "r", encoding="utf-8") as f:
                books_text = f.read()
        except Exception as e:
            logger.error(f"Error reading books.txt: {e}")
            raise

        # Initialize the tokenizer
        if self.args.tokenizer:
            tokenizer = AutoTokenizer.from_pretrained(self.args.tokenizer)
        else:
            logger.error("Tokenizer is required for custom input type")
            raise ValueError("Tokenizer is required for custom input type")

        # Generate a list of random tokens to insert at the beginning of each prompt
        random_tokens = []
        for _ in range(self.prompt_count):
            # Generate a random token (a random word)
            random_token = "".join(random.choices(string.ascii_lowercase, k=5))
            random_tokens.append(random_token)

        # Create prompts by truncating the text to the specified length
        prompts = []
        for i in range(self.prompt_count):
            # Insert the random token at the beginning
            prompt_with_token = random_tokens[i] + " " + books_text

            # Tokenize and truncate to random_input length
            tokenized_prompt = tokenizer(
                prompt_with_token,
                max_length=self.args.random_input,
                truncation=True,
                return_tensors="pt",
            ).input_ids

            # Convert token IDs back to text
            truncated_prompt = tokenizer.decode(tokenized_prompt[0], skip_special_tokens=True)
            prompts.append(truncated_prompt)

        return prompts

    def generate_random_prompts(self):
        # 5 letter words
        random_prompts = [
            " ".join(
                "".join(random.choices(string.ascii_lowercase, k=5))
                for _ in range(self.args.random_input)
            )
            for _ in range(self.prompt_count)
        ]
        # use tokenizer to return prompt for proper length
        logger.info(
            f"If a tokenizer was provided we'll truncate the prompts to {self.args.random_input}"
        )

        if self.args.tokenizer:
            tokenizer = AutoTokenizer.from_pretrained(self.args.tokenizer)
            tokenized_prompts = [
                tokenizer(
                    prompt, max_length=self.args.random_input, truncation=True, return_tensors="pt"
                ).input_ids
                for prompt in random_prompts
            ]

            # Convert token IDs back to prompts for more readability
            truncated_prompts = [
                tokenizer.decode(prompt[0], skip_special_tokens=True)
                for prompt in tokenized_prompts
            ]

            return truncated_prompts
        else:
            return random_prompts

    def read_prompts_from_file(self):
        with open(self.args.input_file, "r") as f:
            prompts = [line.strip() for line in f if line.strip()]
        return self._handle_prompt_count(prompts)

    def read_prompts_from_stdin(self):
        prompts = []
        logger.info("\nEnter your prompts. Press Enter after each prompt.")
        logger.info(f"Enter up to {self.prompt_count} prompts.")
        logger.info(
            "When you're finished, press Ctrl+D (Unix) or Ctrl+Z (Windows) followed by Enter."
        )

        for i in range(1, self.prompt_count + 1):
            try:
                prompt = input(f"Prompt {i}: ").strip()
                if prompt:
                    prompts.append(prompt)
                else:
                    logger.info("Empty prompt ignored. Continue with the next or finish input.")
            except EOFError:
                break

        if not prompts:
            logger.info("No prompts were entered. Exiting.")
            sys.exit(1)

        return self._handle_prompt_count(prompts)

    def _handle_prompt_count(self, prompts):
        if len(prompts) < self.prompt_count:
            logger.info(
                f"\nWarning: Only {len(prompts)} prompt(s) available. Using all available prompts."
            )
        elif len(prompts) > self.prompt_count:
            logger.info(
                f"\nWarning: {len(prompts)} prompts found. Using first {self.prompt_count} prompts."
            )
            prompts = prompts[: self.prompt_count]
        return prompts
