#!/usr/bin/env python
# cli.py - Command Line Interface
# ===============================

"""
ContextWormhole CLI - Command line interface for ContextWormhole

This module provides a command-line interface for using ContextWormhole
to process long context inputs with transformer models.
"""

import argparse
import sys
import logging
from typing import List, Optional

from contextwormhole.core import (
    ContextWormholeModel,
    ExtendedContextConfig,
    create_extended_model,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command line arguments.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="ContextWormhole - Extend context length in transformer models"
    )

    # Main arguments
    parser.add_argument(
        "--model", "-m", type=str, default="gpt2", help="Model path or name"
    )
    parser.add_argument(
        "--input", "-i", type=str, help="Input text or file path (use - for stdin)"
    )
    parser.add_argument(
        "--output", "-o", type=str, help="Output file path (defaults to stdout)"
    )
    parser.add_argument(
        "--strategy",
        "-s",
        type=str,
        choices=["sliding_window", "hierarchical", "attention_sink"],
        default="sliding_window",
        help="Context extension strategy",
    )

    # Configuration options
    config_group = parser.add_argument_group("Configuration")
    config_group.add_argument(
        "--window-size", type=int, default=512, help="Size of sliding window"
    )
    config_group.add_argument(
        "--overlap", type=int, default=50, help="Overlap between windows"
    )
    config_group.add_argument(
        "--chunk-size", type=int, default=256, help="Size of chunks for hierarchical processing"
    )
    config_group.add_argument(
        "--summary-length", type=int, default=64, help="Length of summaries in hierarchical processing"
    )
    config_group.add_argument(
        "--sink-tokens", type=int, default=4, help="Number of sink tokens for attention sink"
    )
    config_group.add_argument(
        "--temperature", type=float, default=0.7, help="Sampling temperature"
    )
    config_group.add_argument(
        "--max-new-tokens", type=int, default=100, help="Maximum new tokens to generate"
    )
    config_group.add_argument(
        "--device", type=str, default=None, help="Device to use (cpu, cuda, cuda:0, etc.)"
    )
    config_group.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )

    return parser.parse_args(args)


def read_input(input_path: str) -> str:
    """Read input from file or stdin.

    Args:
        input_path: Path to input file or "-" for stdin

    Returns:
        Input text
    """
    if input_path == "-":
        logger.info("Reading from stdin...")
        return sys.stdin.read()
    else:
        logger.info(f"Reading from file: {input_path}")
        with open(input_path, "r", encoding="utf-8") as f:
            return f.read()


def write_output(output_path: Optional[str], text: str) -> None:
    """Write output to file or stdout.

    Args:
        output_path: Path to output file or None for stdout
        text: Text to write
    """
    if output_path:
        logger.info(f"Writing to file: {output_path}")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)
        sys.stdout.write("\n")


def main(args: Optional[List[str]] = None) -> int:
    """Main entry point for the CLI.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code
    """
    parsed_args = parse_args(args)

    try:
        # Create configuration
        config = ExtendedContextConfig(
            window_size=parsed_args.window_size,
            overlap=parsed_args.overlap,
            chunk_size=parsed_args.chunk_size,
            summary_length=parsed_args.summary_length,
            sink_tokens=parsed_args.sink_tokens,
            temperature=parsed_args.temperature,
            verbose=parsed_args.verbose,
        )

        # Create model
        logger.info(f"Loading model: {parsed_args.model}")
        model = create_extended_model(
            parsed_args.model, device=parsed_args.device, **config.__dict__
        )

        # Read input
        if parsed_args.input:
            input_text = read_input(parsed_args.input)
        else:
            logger.error("No input provided. Use --input or pipe content to stdin.")
            return 1

        # Process with selected strategy
        logger.info(f"Processing with strategy: {parsed_args.strategy}")
        if parsed_args.strategy == "sliding_window":
            output = model.sliding_window_generate(
                input_text, max_new_tokens=parsed_args.max_new_tokens
            )
        elif parsed_args.strategy == "hierarchical":
            output = model.hierarchical_generate(
                input_text, max_new_tokens=parsed_args.max_new_tokens
            )
        elif parsed_args.strategy == "attention_sink":
            output = model.attention_sink_generate(
                input_text, max_new_tokens=parsed_args.max_new_tokens
            )
        else:
            logger.error(f"Unknown strategy: {parsed_args.strategy}")
            return 1

        # Write output
        write_output(parsed_args.output, output)
        return 0

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())