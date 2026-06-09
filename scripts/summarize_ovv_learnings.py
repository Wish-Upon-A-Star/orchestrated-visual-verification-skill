#!/usr/bin/env python3
"""Summarize OVV learning records and propose skill patch candidates."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


PATCH_HINTS = {
    "requirements": "Strengthen the task-map requirement extraction rule or add a stricter fixture for missing acceptance criteria.",
    "evidence": "Strengthen the completion audit to require requirement-to-evidence mapping before final signoff.",
    "orchestration_decision": "Clarify when solo execution is acceptable and when validators/workers are required.",
    "visual_browser": "Add or tighten a hard gate for browser, screenshot, viewport, or rendered artifact evidence on user-visible work.",
    "review_rounds": "Tighten final report requirements for counted review rounds and per-round inspection notes.",
    "issue_fix_recheck": "Require issue/fix/re-check accounting even when the result is 'none found'.",
    "regression": "Add an adjacent-feature regression check prompt to the quick-start path.",
    "limitations": "Require explicit unresolved limitation accounting or 'none known after checks'.",
    "usage": "Require usage instructions for every delivered artifact or feature.",
    "no_vague_completion": "Add stronger anti-pattern checks for completion claims without evidence.",
}


def default_log_path() -> Path:
    return Path.cwd() / "memory" / "ovv_skill_learnings.jsonl"


def read_records(path: Path) -> list[dict]:
    records = []
    if not path.exists():
        return records
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as error:
            records.append({
                "failure": "invalid_record",
                "task": str(path),
                "lesson": f"Invalid JSONL line {line_number}: {error}",
                "resolution": "Fix or remove the malformed learning record.",
            })
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, default=default_log_path(), help="JSONL learning log path")
    parser.add_argument("--min-count", type=int, default=2, help="Minimum repeated failures before patch candidate")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args()

    records = read_records(args.log)
    counts = Counter(record.get("failure", "unknown") for record in records)
    examples = defaultdict(list)
    for record in records:
        failure = record.get("failure", "unknown")
        if len(examples[failure]) < 3:
            examples[failure].append(record)

    candidates = []
    for failure, count in counts.most_common():
        if count < args.min_count:
            continue
        candidates.append({
            "failure": failure,
            "count": count,
            "suggested_patch": PATCH_HINTS.get(
                failure,
                "Inspect repeated records and add a targeted rule, audit check, or fixture only if it reduces real misses.",
            ),
            "examples": examples[failure],
        })

    payload = {
        "log": str(args.log),
        "total_records": len(records),
        "counts": dict(counts.most_common()),
        "patch_candidates": candidates,
    }

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"# OVV Learning Summary")
    print()
    print(f"- Log: `{args.log}`")
    print(f"- Total records: {len(records)}")
    print()
    print("## Failure Counts")
    if counts:
        for failure, count in counts.most_common():
            print(f"- `{failure}`: {count}")
    else:
        print("- none")
    print()
    print("## Patch Candidates")
    if candidates:
        for candidate in candidates:
            print(f"- `{candidate['failure']}` ({candidate['count']}): {candidate['suggested_patch']}")
    else:
        print(f"- none at min-count {args.min_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
