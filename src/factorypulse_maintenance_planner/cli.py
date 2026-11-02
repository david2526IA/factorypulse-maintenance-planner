from __future__ import annotations

import argparse
import json
from pathlib import Path

from .planner import plan, read_jsonl, write_json


def main() -> None:
    parser = argparse.ArgumentParser(description="Create human-reviewed maintenance recommendations.")
    parser.add_argument("input", type=Path, help="FactoryPulse anomaly JSONL")
    parser.add_argument("--output", type=Path, default=Path("maintenance_recommendations.json"))
    args = parser.parse_args()
    recommendations = plan(read_jsonl(args.input))
    write_json(args.output, recommendations)
    print(json.dumps({"recommendations": len(recommendations), "output": str(args.output)}))
