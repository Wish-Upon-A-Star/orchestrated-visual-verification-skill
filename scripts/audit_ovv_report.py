#!/usr/bin/env python3
"""Score an OVV plan or final report for evidence completeness.

This is a lightweight audit, not a correctness proof. It improves outcomes by
making evidence-free completion claims fail and by optionally recording failed
categories for future skill improvement.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


CHECKS = [
    {
        "id": "requirements",
        "weight": 12,
        "patterns": [
            r"\brequirements?\b",
            r"\bacceptance criteria\b",
            r"\bexplicit requirements?\b",
            r"\bimplied requirements?\b",
            r"\bnon-goals?\b",
        ],
        "hint": "List explicit/implied requirements or acceptance criteria.",
    },
    {
        "id": "evidence",
        "weight": 14,
        "patterns": [
            r"\bevidence\b",
            r"\bverified\b",
            r"\bverification results?\b",
            r"\bcommand\b",
            r"\boutput\b",
            r"\blog[s]?\b",
            r"\binspected\b",
        ],
        "hint": "Map requirements to concrete evidence such as commands, screenshots, logs, or inspected files.",
    },
    {
        "id": "orchestration_decision",
        "weight": 8,
        "patterns": [
            r"\borchestration decision\b",
            r"\borchestration\b",
            r"\bsolo execution\b",
            r"\bworker\b",
            r"\bvalidator\b",
        ],
        "hint": "Explain why the work was solo or orchestrated, with role/validator boundaries if used.",
    },
    {
        "id": "visual_browser",
        "weight": 12,
        "patterns": [
            r"\bscreenshot\b",
            r"\bbrowser\b",
            r"\bplaywright\b",
            r"\bviewport\b",
            r"\bmobile\b",
            r"\bdesktop\b",
            r"\bvisual\b",
            r"\brendered\b",
        ],
        "hint": "For user-visible work, include browser/screenshot/viewport or equivalent rendered evidence.",
    },
    {
        "id": "review_rounds",
        "weight": 12,
        "patterns": [
            r"\breview rounds? actually performed\b",
            r"\bround\s+\d+\b",
            r"\breview\s+\d+\b",
            r"\bpass\s+\d+\b",
        ],
        "hint": "Record distinct review rounds and what each inspected.",
    },
    {
        "id": "issue_fix_recheck",
        "weight": 12,
        "patterns": [
            r"\bissue[s]? found\b",
            r"\bbugs? found\b",
            r"\bfixed\b",
            r"\brechecked\b",
            r"\bre-checked\b",
            r"\bresolved\b",
            r"\bfix(?:ed|es)?\b",
        ],
        "hint": "Report issues found, fixes applied, and re-checks after fixes.",
    },
    {
        "id": "regression",
        "weight": 8,
        "patterns": [
            r"\bregression[s]? checked\b",
            r"\bregression\b",
            r"\badjacent\b",
            r"\bneighboring\b",
            r"\brelated features?\b",
        ],
        "hint": "State adjacent/regression checks and their results.",
    },
    {
        "id": "limitations",
        "weight": 8,
        "patterns": [
            r"\bremaining limitations?\b",
            r"\bunresolved\b",
            r"\bknown issue[s]?\b",
            r"\bcould not\b",
            r"\bnot run\b",
            r"\bnone known\b",
        ],
        "hint": "Account for unresolved limitations or explicitly state none known after checks.",
    },
    {
        "id": "usage",
        "weight": 6,
        "patterns": [
            r"\bhow to use\b",
            r"\busage\b",
            r"\bopen\b",
            r"\brun\b",
            r"\binvoke\b",
        ],
        "hint": "Explain how to use the deliverable.",
    },
    {
        "id": "no_vague_completion",
        "weight": 8,
        "negative_patterns": [
            r"\bimplemented\b.{0,40}\b(no tests|not tested|untested)\b",
            r"\breviewed thoroughly\b(?![\s\S]{0,500}\bround\b)",
            r"\bdone\b.{0,80}\btrust me\b",
        ],
        "hint": "Avoid vague completion claims without evidence.",
    },
]


def default_log_path() -> Path:
    return Path.cwd() / "memory" / "ovv_skill_learnings.jsonl"


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)


def audit_text(text: str, threshold: int) -> dict:
    possible = sum(check["weight"] for check in CHECKS)
    score = 0
    failures = []

    for check in CHECKS:
        negative_patterns = check.get("negative_patterns", [])
        if negative_patterns:
            passed = not has_any(text, negative_patterns)
        else:
            passed = has_any(text, check.get("patterns", []))
        if passed:
            score += check["weight"]
        else:
            failures.append({"id": check["id"], "hint": check["hint"]})

    percent = round(score / possible * 100)
    status = "PASS" if percent >= threshold and not failures else "FAIL"
    return {
        "status": status,
        "score": score,
        "possible": possible,
        "percent": percent,
        "threshold": threshold,
        "failures": failures,
    }


def record_failures(path: Path, payload: dict, learning_log: Path) -> None:
    if payload["status"] == "PASS":
        return

    learning_log.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    with learning_log.open("a", encoding="utf-8") as handle:
        for failure in payload["failures"]:
            record = {
                "timestamp": timestamp,
                "task": str(path),
                "failure": failure["id"],
                "lesson": failure["hint"],
                "resolution": "Audit failure recorded automatically; fix the current artifact, then update the skill only if this repeats.",
                "source": "audit_ovv_report.py",
                "score_percent": payload["percent"],
            }
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="Markdown plan or final report to audit")
    parser.add_argument("--threshold", type=int, default=78, help="Passing score threshold")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument(
        "--record-failures",
        action="store_true",
        help="Append failed categories to the OVV learning log",
    )
    parser.add_argument(
        "--learning-log",
        type=Path,
        default=default_log_path(),
        help="JSONL learning log path for --record-failures",
    )
    args = parser.parse_args()

    if not args.path.exists():
        print(f"ERROR: file not found: {args.path}", file=sys.stderr)
        return 2

    text = args.path.read_text(encoding="utf-8", errors="replace")
    payload = audit_text(text, args.threshold)

    if args.record_failures:
        record_failures(args.path, payload, args.learning_log)

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["status"] == "PASS" else 1

    print(f"OVV audit: {payload['status']}")
    print(f"Score: {payload['score']}/{payload['possible']} ({payload['percent']}%)")
    print(f"Threshold: {payload['threshold']}%")

    if payload["failures"]:
        print("Missing or weak categories:")
        for failure in payload["failures"]:
            print(f"- {failure['id']}: {failure['hint']}")
        if args.record_failures:
            print(f"Recorded failures: {args.learning_log}")
    else:
        print("All audit categories present.")

    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
