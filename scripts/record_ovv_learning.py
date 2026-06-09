#!/usr/bin/env python3
"""Record a real OVV miss so the skill can improve over time."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def default_log_path() -> Path:
    cwd = Path.cwd()
    memory = cwd / "memory"
    if memory.exists() or cwd.name:
        return memory / "ovv_skill_learnings.jsonl"
    return Path("ovv_skill_learnings.jsonl")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", required=True, help="Short task name or context")
    parser.add_argument("--failure", required=True, help="Failed category, e.g. visual_browser")
    parser.add_argument("--lesson", required=True, help="Reusable lesson from the miss")
    parser.add_argument("--resolution", required=True, help="How the current work was fixed")
    parser.add_argument("--log", type=Path, default=default_log_path(), help="JSONL learning log path")
    args = parser.parse_args()

    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "task": args.task,
        "failure": args.failure,
        "lesson": args.lesson,
        "resolution": args.resolution,
    }

    args.log.parent.mkdir(parents=True, exist_ok=True)
    with args.log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")

    print(f"Recorded OVV learning: {args.log}")
    print(json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
