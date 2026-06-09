# Orchestrated Visual Verification (OVV)

OVV is a Codex skill for work that should not end at "implemented." It turns broad coding, UI, game, workflow, or agent-system tasks into an evidence-driven loop with orchestration decisions, visual verification, repeated review, measurable audit gates, and a self-improvement log.

Short name: **OVV**

Skill invocation:

```text
$orchestrated-visual-verification
```

Natural-language invocation:

```text
Use OVV to plan, implement, visually verify, review, and report this work.
```

## What This Skill Does

OVV makes Codex answer five questions before claiming completion:

1. What exactly was required?
2. Was solo execution enough, or was orchestration with workers/validators needed?
3. What evidence proves each requirement?
4. If the work is user-visible, what browser, screenshot, viewport, or rendered evidence proves the UI actually looks right?
5. What review rounds happened, what issues were found, and what was rechecked after fixes?

The skill includes:

- `SKILL.md`: the Codex skill instructions.
- `references/feasible-upgrades.md`: 125 practical workflow and verification improvements.
- `references/eval-fixtures.md`: weak/strong report fixtures for testing the skill.
- `scripts/audit_ovv_report.py`: scores plans or final reports for evidence completeness.
- `scripts/record_ovv_learning.py`: records real misses into a JSONL learning log.
- `scripts/summarize_ovv_learnings.py`: summarizes repeated misses and proposes skill patch candidates.
- `agents/openai.yaml`: UI metadata for Codex skill lists.

## Why It Exists

Many agent workflows fail in the same ways:

- requirements are vague or incomplete,
- "done" is claimed without evidence,
- UI work is checked only by code or tests, not by screenshots/browser state,
- review rounds are summarized but not actually performed,
- recurring mistakes are forgotten instead of being fed back into the workflow.

OVV is designed to make those weak completions fail early. It is not a replacement for tests, Playwright, manual review, or product judgment. It is a forcing function that makes missing evidence visible.

## Installation

### Windows PowerShell

Clone the repo, then copy it into your Codex skills directory:

```powershell
git clone https://github.com/Wish-Upon-A-Star/orchestrated-visual-verification-skill.git
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force orchestrated-visual-verification-skill "$env:USERPROFILE\.codex\skills\orchestrated-visual-verification"
```

Restart Codex after installing so the skill list refreshes.

### macOS / Linux

```bash
git clone https://github.com/Wish-Upon-A-Star/orchestrated-visual-verification-skill.git
mkdir -p "$HOME/.codex/skills"
cp -R orchestrated-visual-verification-skill "$HOME/.codex/skills/orchestrated-visual-verification"
```

Restart Codex after installing so the skill list refreshes.

## Basic Usage

Use the skill explicitly:

```text
$orchestrated-visual-verification
Build this feature and verify it with browser screenshots and review rounds.
```

Or use the short name:

```text
OVV 써서 이 작업을 구현, 시각 검증, 리뷰 라운드까지 끝내줘.
```

For a report-only audit:

```bash
python ~/.codex/skills/orchestrated-visual-verification/scripts/audit_ovv_report.py final-report.md
```

On Windows:

```powershell
python "$env:USERPROFILE\.codex\skills\orchestrated-visual-verification\scripts\audit_ovv_report.py" final-report.md
```

## Audit Script

`audit_ovv_report.py` checks whether a plan or final report contains the evidence OVV expects.

It scores these categories:

- requirements,
- evidence,
- orchestration decision,
- visual/browser evidence,
- review rounds,
- issue/fix/recheck loop,
- regression checks,
- limitations,
- usage instructions,
- vague completion anti-patterns.

Run:

```bash
python scripts/audit_ovv_report.py final-report.md
```

JSON output:

```bash
python scripts/audit_ovv_report.py final-report.md --json
```

Record failures into the learning log:

```bash
python scripts/audit_ovv_report.py final-report.md --record-failures
```

Use a custom learning log:

```bash
python scripts/audit_ovv_report.py final-report.md --record-failures --learning-log memory/ovv_skill_learnings.jsonl
```

Important: passing the audit does not prove the underlying product is correct. It proves that the report contains the expected evidence categories.

## Self-Improvement Loop

OVV is designed to improve from real misses:

1. Run the audit.
2. Fix the current artifact if the audit fails.
3. Record failures automatically with `--record-failures`.
4. Summarize repeated failures.
5. Convert repeated failure categories into targeted skill patches or new fixtures.
6. Re-run the fixtures after changing the skill.

Summarize the learning log:

```bash
python scripts/summarize_ovv_learnings.py --log memory/ovv_skill_learnings.jsonl --min-count 2
```

Example output:

```text
## Patch Candidates
- `visual_browser` (3): Add or tighten a hard gate for browser, screenshot, viewport, or rendered artifact evidence on user-visible work.
- `evidence` (2): Strengthen the completion audit to require requirement-to-evidence mapping before final signoff.
```

Manual learning record:

```bash
python scripts/record_ovv_learning.py \
  --task "settings panel" \
  --failure visual_browser \
  --lesson "UI signoff needs screenshot evidence" \
  --resolution "Added desktop and mobile screenshot checks"
```

## Verification Fixtures

The repository includes fixtures in `references/eval-fixtures.md`.

Expected behavior:

- weak report: FAIL,
- strong report: PASS,
- UI report without visual evidence: FAIL,
- repeated weak failures: patch candidates generated.

Quick local smoke test:

```bash
mkdir -p tmp
printf "Done. I implemented the UI and reviewed it thoroughly. Tests passed.\n" > tmp/weak.md
python scripts/audit_ovv_report.py tmp/weak.md --record-failures --learning-log tmp/learnings.jsonl
python scripts/audit_ovv_report.py tmp/weak.md --record-failures --learning-log tmp/learnings.jsonl
python scripts/summarize_ovv_learnings.py --log tmp/learnings.jsonl --min-count 2
```

## When To Use OVV

Use OVV for:

- UI/frontend work that needs browser or screenshot verification,
- game UI or visual state work,
- multi-file coding tasks with regression risk,
- tasks requiring exact review rounds,
- agent prompt or workflow design,
- work where completion must be evidence-backed,
- tasks that may need orchestration but should not use it blindly.

Do not use the full OVV loop for:

- tiny one-line edits,
- simple factual answers,
- tasks where no implementation or verification claim is being made.

For small work, use the lightweight path: extract requirements, make the edit, run the narrowest meaningful check, self-review the diff, and report evidence.

## Repository Layout

```text
.
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── eval-fixtures.md
│   └── feasible-upgrades.md
└── scripts/
    ├── audit_ovv_report.py
    ├── record_ovv_learning.py
    └── summarize_ovv_learnings.py
```

## Development

Run syntax checks:

```bash
python -m py_compile scripts/audit_ovv_report.py scripts/record_ovv_learning.py scripts/summarize_ovv_learnings.py
```

Run a weak-report audit:

```bash
printf "Done. I implemented the UI and reviewed it thoroughly. Tests passed.\n" > weak.md
python scripts/audit_ovv_report.py weak.md
```

The weak report should fail.

## License

MIT
