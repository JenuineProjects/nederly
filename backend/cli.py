"""End-to-end test runner for the Nederly agent pipeline.

Usage (from backend/ dir, with venv active and ANTHROPIC_API_KEY set):

    python cli.py paste "goedemorgen, dank je wel, tot ziens"
    python cli.py topic "ordering coffee"

Prints the resulting Exercise Spec as pretty JSON. Useful for iterating on
agent prompts before the mobile app exists.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

from agents.manager import generate
from schemas import GenerateRequest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["paste", "topic"])
    parser.add_argument("text")
    parser.add_argument("--max-items", type=int, default=8)
    args = parser.parse_args()

    req = GenerateRequest(mode=args.mode, text=args.text, max_items=args.max_items)
    spec = generate(req)
    print(json.dumps(spec.model_dump(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
