---
name: orchestrated-visual-verification
description: Use when a task needs Codex to design or improve a high-rigor workflow that combines orchestration, agent routing, implementation gates, browser or screenshot-based visual QA, repeated review rounds, and final evidence-based completion checks. Also use when the user asks to find many feasible workflow improvements, build a powerful Codex skill, or combine ODRV, verify, Playwright, frontend, and multi-agent validation practices.
---

# Orchestrated Visual Verification

## Purpose

Use this skill to turn broad product, UI, game, workflow, or agent-system work into a governed loop:

1. map the real objective,
2. choose orchestration only where it helps,
3. split work into owned surfaces,
4. validate with code, runtime, browser, screenshot, and product checks,
5. fix findings,
6. repeat review until the requested bar is met,
7. report only what current evidence proves.

This skill is intentionally stricter than a normal implementation loop. It is for tasks where "looks implemented" is not enough.

## Relationship To Other Skills

Use these skills as building blocks instead of replacing them:

- `odrv` or `orchestrating-design-research-verification`: top-level routing when design, research, implementation, and verification all matter.
- `verify`: main evidence, implementation, and review loop.
- `general-work-orchestrator`: worker roles, task slicing, review gates, retries, and merge discipline.
- `frontend-skill`: UI composition, hierarchy, responsive layout, visual polish, and product-surface quality.
- `playwright` or repo-specific browser tools: real browser inspection, screenshots, interaction flow checks, and visual evidence.
- `verification-before-completion`: final no-fake-success gate when available.
- `agents-work-enforcer`: literal AGENTS.md compliance, review-round counts, and final report contracts.

If a referenced skill conflicts with local repo rules, local repo rules win.

## Quick Start

Use this sequence:

1. **Contract**: extract explicit and implied requirements, review count, final report format, non-goals, and no-early-exit rules.
2. **Evidence map**: identify files, routes, screens, commands, assets, data records, and external services that can prove completion.
3. **Orchestration decision**: decide whether to work solo, split into roles, or use validators. Use orchestration only when it reduces risk.
4. **Design gate**: for UX, UI, workflow, game, or agent behavior changes, define the intended user outcome and failure modes before editing.
5. **Implementation**: make scoped changes in owned files only. Preserve user changes and avoid unrelated refactors.
6. **Visual verification**: inspect the live UI or generated artifact with browser/screenshot checks where visual behavior matters.
7. **Review rounds**: perform the requested number of distinct rounds, or at least one code review and one product/visual review for nontrivial work.
8. **Fix and restart affected checks**: if a defect is found, fix it, verify the fix, and re-check related areas before continuing.
9. **Completion audit**: prove every requirement with current evidence. Treat missing evidence as incomplete.
10. **Report**: include changes, evidence, review rounds, defects found and resolved, remaining limitations, and usage instructions.

## Measured Improvement Contract

This skill must improve outcomes by making weak work fail earlier. For nontrivial tasks, create or preserve an audit trail that another reviewer can score:

- requirements and implied requirements,
- chosen execution shape and why orchestration was or was not used,
- evidence per requirement,
- visual/browser checks when user-visible behavior exists,
- review rounds actually performed,
- issues found, fixes applied, and re-checks,
- unresolved limitations.

When practical, run the bundled audit script before final signoff:

```bash
python <skill-dir>/scripts/audit_ovv_report.py <final-report-or-plan.md>
```

To make audit failures feed the learning loop automatically:

```bash
python <skill-dir>/scripts/audit_ovv_report.py <final-report-or-plan.md> --record-failures
```

Passing the audit script does not prove the task is correct. Failing it means the response is missing evidence expected by this skill and should be fixed before claiming completion.

## Task Map

Before editing, write a compact map:

- Objective: what final state must be true.
- Deliverables: files, UI screens, docs, skill folders, generated assets, tests, or commands.
- Affected surfaces: code, data, CSS, templates, assets, browser flows, docs, automation, prompts, external connectors.
- Risk level: low, normal, high, or intensive.
- Required skills: select the minimal relevant set.
- Verification evidence: commands, screenshots, logs, rendered pages, payload checks, file inspections, or review artifacts.
- Stop conditions: credentials, missing tool access, contradictory requirements, or destructive action requiring approval.

## Orchestration Decision

Choose the smallest reliable execution shape:

| Situation | Execution shape |
| --- | --- |
| Single-file or narrow doc/skill edit | Solo implementation plus self-review |
| Multi-file but tightly coupled code | Solo implementation plus staged verification |
| Disjoint work surfaces | Worker roles with non-overlapping ownership |
| UI or product quality risk | Add visual/product validator |
| Runtime behavior risk | Add runtime/API validator |
| Asset or localization risk | Add asset/locale validator |
| User requested exact review rounds | Solo or validator reviews, counted literally |
| Merge from multiple outputs | Review each output before merge, then verify merged result |

Do not create workers for ceremony. A worker must have a bounded owned output and an explicit review gate.

## Review Gates

For each task or worker output, define:

- Acceptance criteria.
- Owned files or artifacts.
- Forbidden scope.
- Evidence required.
- Pass/fail criteria.
- Retry owner if failed.

Valid review outcomes:

- `pass`: evidence proves the output meets the criteria.
- `retry`: concrete defects exist and must be fixed.
- `manual_review`: the next decision needs user input, credentials, or external approval.

Avoid soft outcomes like "mostly fine."

## Visual Verification Ladder

Use the first rung that matches the risk, then climb when evidence is weak.

1. **Static inspection**: HTML/CSS/template or artifact file review.
2. **Build or render check**: app builds, template renders, generated artifact opens.
3. **Browser smoke**: open the target page, inspect the main viewport, and exercise one core action.
4. **Screenshot review**: capture desktop and mobile or relevant responsive states.
5. **Interaction flow**: click, type, navigate, trigger loading/empty/error states.
6. **Pixel or canvas check**: verify canvas/image/3D/rendered media is nonblank and framed.
7. **Regression path**: revisit adjacent pages or flows likely to be affected.
8. **Cross-surface consistency**: compare frontend labels, API payloads, localized text, assets, and docs.

Use repo-specific browser rules when present. In this repository, Playwright validation defaults to `http://localhost:5050` and full-screen style review windows.

## 100+ Improvement Catalog

When the user asks for many improvement ideas, or when designing a reusable workflow, read `references/feasible-upgrades.md`. Use it as a menu, not a mandate:

- select only improvements that fit the current task,
- prefer items with direct evidence and cheap verification,
- avoid adding process weight that does not reduce real risk,
- turn selected items into concrete checks or skill rules.

The catalog includes a source basis section. Use that section to keep the selected checks grounded in inspected local skills and official guidance instead of treating the list as free-floating advice.

## Evaluation Harness

For skill-quality work or when the user challenges whether this skill actually helps, read `references/eval-fixtures.md` and use the audit script. The harness improves performance by forcing three measurable behaviors:

1. weak reports without evidence fail,
2. strong reports with requirement coverage and review evidence pass,
3. visual/UI work must include explicit visual evidence instead of only code/test claims.

## Self-Improvement Loop

This skill should improve from failures instead of only reporting them.

After each substantial use, especially when the user challenges quality or a review finds a missed issue:

1. Run or mentally apply the OVV audit categories to the plan/report.
2. If a category fails, fix the current work first.
3. Record the learning. Prefer automatic audit recording:

   ```bash
   python <skill-dir>/scripts/audit_ovv_report.py <final-report-or-plan.md> --record-failures
   ```

   For misses found outside the audit script, record manually:

   ```bash
   python <skill-dir>/scripts/record_ovv_learning.py --task "<short task>" --failure "<category>" --lesson "<what should change>" --resolution "<how it was fixed>"
   ```

4. Periodically summarize the learning log:

   ```bash
   python <skill-dir>/scripts/summarize_ovv_learnings.py --min-count 2
   ```

5. If the same failure category appears repeatedly, use the summary's patch candidates to update this skill, the audit script, or `references/feasible-upgrades.md` with a sharper rule.
6. Re-run the audit script and relevant fixtures after the skill update.

Use this loop only for real misses, weak evidence, repeated user corrections, or audit failures. Do not bloat the skill with speculative rules.

## Intensive Mode

Use intensive mode when the user asks for deep review, many review rounds, production-safe validation, or no early exit.

In intensive mode:

- assume subtle defects exist until checked,
- inspect adjacent code and integration points,
- review implementation, user outcome, UI/UX, edge cases, regressions, maintainability, and evidence quality separately,
- keep a short note per round,
- fix issues immediately and re-check affected areas,
- do not compress requested review rounds into one pass.

## Completion Audit

Before claiming success, verify each explicit requirement:

- requirement text,
- evidence source,
- result: proved, contradicted, incomplete, weak, or missing,
- action taken if not proved.

Completion requires all required items to be proved or honestly marked as unresolved blockers.

## Final Report

Use the user's requested format when provided. Otherwise report:

- final deliverable,
- files changed or artifacts created,
- selected workflow and why,
- review rounds actually performed,
- issues found and how each was resolved,
- visual/browser checks performed,
- regression checks performed,
- remaining limitations,
- how to use the deliverable.
