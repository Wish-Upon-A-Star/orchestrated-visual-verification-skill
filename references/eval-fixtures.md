# Evaluation Fixtures

Use these fixtures to check whether `orchestrated-visual-verification` is producing measurably better work. They are not user-facing templates; they are small tests for the skill's own quality gates.

## What The Harness Measures

The bundled script `scripts/audit_ovv_report.py` checks whether a plan or final report contains evidence of:

- requirement extraction,
- evidence mapping,
- orchestration decision,
- visual/browser verification where relevant,
- distinct review rounds,
- issue/fix/re-check loop,
- regression checks,
- unresolved limitation handling,
- usage instructions.

The script intentionally scores the artifact, not the underlying product. It catches weak completion claims and missing evidence; it does not replace tests, browser inspection, or human judgment.

## Fixture 1: Weak Report Should Fail

```markdown
Done. I implemented the UI and reviewed it thoroughly. Tests passed.
```

Expected result:

- score below passing threshold,
- missing requirements,
- missing evidence,
- missing visual checks,
- missing review round details,
- missing unresolved issue accounting.

## Fixture 2: Strong Report Should Pass

```markdown
### example-project ###

#1. Problem -> Method -> Final Result
Problem: The user asked for a responsive settings panel.
Method: Extracted requirements, inspected existing CSS, implemented scoped template and stylesheet changes, ran browser checks.
Final Result: Settings panel opens, closes, preserves form state, and fits desktop/mobile.

Requirements:
- responsive settings panel
- open and close behavior
- no text overflow
- preserve existing form state

Evidence:
- `npm test` passed for settings reducer tests.
- Browser smoke opened `/settings` and clicked open/close controls.
- Desktop screenshot: `output/playwright/settings-desktop.png`.
- Mobile screenshot: `output/playwright/settings-mobile.png`.

Orchestration decision:
- Solo execution because the change touched one template and one stylesheet.

Review rounds actually performed: 2

Round 1:
- inspected code correctness, state transitions, error handling, and regression risk.
- found missing Escape close behavior.
- fixed Escape close and rechecked open/close.

Round 2:
- inspected visual layout, desktop/mobile screenshots, text overflow, and empty/error states.
- found no unresolved issues.

Regressions checked:
- adjacent profile panel still opens.
- existing form submit test still passes.

Bugs found at completion time:
- none known after the checks above.

Remaining limitations:
- no cross-browser matrix was run.

How to use:
- open `/settings`, click the settings button, edit fields, close or press Escape.
```

Expected result:

- score meets passing threshold,
- all core evidence categories present,
- visual evidence present,
- issue/fix/re-check loop present.

## Fixture 3: UI Report Without Visual Evidence Should Fail

```markdown
Implemented the landing page. Requirements were reviewed. Unit tests passed. No issues remain.
```

Expected result:

- fails visual/browser evidence checks,
- asks for screenshot, browser, viewport, or equivalent rendered artifact evidence.

## How To Use During Skill Development

1. Save one fixture as a temporary markdown file.
2. Run `python scripts/audit_ovv_report.py <fixture.md>`.
3. Confirm weak fixtures fail and strong fixtures pass.
4. Run weak fixtures with `--record-failures --learning-log <tmp-log.jsonl>`.
5. Run `python scripts/summarize_ovv_learnings.py --log <tmp-log.jsonl> --min-count 2`.
6. Confirm repeated failure categories produce patch candidates.
7. When editing the skill, add or adjust checks only if they catch real missing evidence without forcing irrelevant ceremony.

## Self-Improvement Fixture

When a task fails because the skill missed an evidence category, record the failure:

```bash
python scripts/record_ovv_learning.py \
  --task "responsive settings panel" \
  --failure "visual_browser" \
  --lesson "UI signoff must include a screenshot or browser inspection artifact" \
  --resolution "Added desktop and mobile screenshot checks before final report"
```

Expected result:

- a JSONL record is appended to `memory/ovv_skill_learnings.jsonl` by default,
- repeated categories can be counted later,
- only real misses become skill changes.

## Automatic Learning Summary Fixture

```bash
python scripts/audit_ovv_report.py weak.md --record-failures --learning-log tmp-learnings.jsonl
python scripts/audit_ovv_report.py weak.md --record-failures --learning-log tmp-learnings.jsonl
python scripts/summarize_ovv_learnings.py --log tmp-learnings.jsonl --min-count 2
```

Expected result:

- weak audit failures are recorded without calling `record_ovv_learning.py` separately,
- repeated categories appear under `Patch Candidates`,
- suggested patches are category-specific instead of generic "review more" advice.
