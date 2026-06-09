# Feasible Upgrade Catalog

Use this catalog when designing an orchestration, visual verification, or high-rigor Codex workflow. Each item is intended to be practical for local repo work, browser apps, document artifacts, skill creation, or agent-system operations.

## Source Basis

This list was distilled from inspected local skills, curated plugin skills, and current official references. Use these source groups when selecting items for a task:

- **Local orchestration and verification skills**: `odrv`, `orchestrating-design-research-verification`, `verify`, `general-work-orchestrator`, `codex-orchestrator`, `agents-work-enforcer`, `verification-before-completion`, and `orchestration`.
- **Local visual and browser skills**: `frontend-skill`, `playwright`, `playwright-interactive`, `screenshot`, `figma`, and `doc`.
- **Curated visual QA skills**: Game Studio `game-playtest`, `game-ui-frontend`, `web-game-foundations`, `phaser-2d-game`, `three-webgl-game`, and `react-three-fiber-game`.
- **Curated full-flow verification skills**: Vercel `verification`, `agent-browser-verify`, `investigation-mode`, `observability`, and `workflow`.
- **Review and issue-follow-up skills**: CodeRabbit `code-review`, GitHub `gh-address-comments`, CircleCI `builds` and `config`.
- **Official guidance checked**: OpenAI evaluation best practices, agent evals, trace grading, agent-builder safety, reasoning best practices, and Playwright visual comparisons.

The items below are filtered for feasibility: each can be executed as a prompt rule, local inspection, file check, browser check, screenshot check, test/eval, review gate, or report requirement without requiring a new platform.

## A. Requirement And Contract Upgrades

1. Convert the user's request into explicit requirements, implied requirements, non-goals, and acceptance criteria before editing.
2. Record the exact final report format up front when the user provides one.
3. Detect exact review-round counts and store them as a literal counter.
4. Distinguish "must finish now" from "goal persists across turns" so progress reports do not redefine success.
5. Add a requirement-to-evidence table before final completion claims.
6. Require every broad requirement to have at least one broad evidence source, not only a narrow spot check.
7. Capture a "do not touch" list for user-owned changes and unrelated dirty files.
8. Define stop conditions before work starts: credentials, destructive action, missing access, or contradictory instructions.
9. Add a non-goal review to prevent unrelated refactors.
10. Include a "what would prove this wrong" question in the task map.

## B. Orchestration Upgrades

11. Choose solo execution for narrow work and reserve workers for independent surfaces.
12. Create worker roles by owned output, not by vague skill level.
13. Require each worker task to include owned files, forbidden scope, expected artifact, and review gate.
14. Split validators by evidence type: code, runtime, UI, product, asset, locale, security, performance.
15. Make validators read-only unless the user explicitly assigns them implementation ownership.
16. Prevent two workers from editing the same file in the same worktree.
17. Use separate branches or worktrees for parallel changes to shared files.
18. Review each worker output before merging it into the main result.
19. Use structured retry prompts that preserve approved parts and name exact fixes.
20. Track unresolved findings in a queue instead of hiding them inside summaries.
21. Add a merge gate that requires every included output to be passed or manually approved.
22. After merge, rerun final verification against the merged state, not the isolated worker state.
23. Record which worker or review level owns each blocker.
24. Keep role counts small unless the work surfaces are truly independent.
25. Treat a validator blocker as product evidence, not as a harness crash, unless the harness itself failed.

## C. Evidence And Research Upgrades

26. Prefer local runtime behavior over documentation when they conflict.
27. Prefer official docs and source code for current APIs and tools.
28. Use external research only when it changes a decision or verifies a current behavior.
29. Expand vague research queries into formal terms, synonyms, constraints, and failure terms.
30. Summarize only decision-relevant findings, not entire articles.
31. Record source priority when sources disagree.
32. For prompting or skill design, check whether the problem is criteria, evals, tools, routing, or model choice before changing wording.
33. Use current files and command output as authoritative over memory.
34. Treat missing evidence as incomplete, not as proof of no issue.
35. Add a "coverage check" to confirm tests or screenshots actually cover the requested behavior.

## D. Implementation Discipline Upgrades

36. Inspect existing code patterns before editing.
37. Use the smallest scoped edit that satisfies the requirement.
38. Preserve formatting and data style of surrounding files.
39. Avoid adding abstractions unless they remove real complexity or match local patterns.
40. Add comments only where they reduce parsing effort for complex code.
41. Keep generated artifacts and manual edits separate when practical.
42. For data files, validate JSON or schema after editing.
43. For large files, search for symbols first and read only relevant ranges.
44. Before editing, identify tests or checks that should fail if the change is wrong.
45. After editing, inspect the diff for unrelated churn.
46. For deleted files, verify the deletion is intended and covered by tests.
47. For localized text, check encoding and escaping.
48. For asset references, verify the file exists and the manifest or record matches.
49. For configuration edits, verify the runtime actually reads the changed config.
50. For generated code, remove unused placeholders and TODO scaffolding before final report.

## E. UI And Visual Verification Upgrades

51. Start UI work with a visual thesis, content plan, and interaction thesis.
52. Verify the first viewport has the primary product or app signal.
53. Check desktop and mobile layout for text overflow.
54. Check that buttons have stable dimensions and do not shift on hover or loading.
55. Verify empty, loading, error, and success states.
56. Confirm modals, drawers, tabs, menus, and popovers close correctly.
57. Confirm keyboard focus order for primary flows.
58. Inspect contrast for text over images or colored surfaces.
59. Check that icons are meaningful and have labels or tooltips where needed.
60. Verify cards are used only where they frame repeated items, modals, or tools.
61. Check that page sections are not nested cards inside cards.
62. Verify imagery is relevant, visible, and not just decorative filler.
63. Inspect whether hero text fits mobile without occluding the next section.
64. Capture screenshots after significant frontend changes.
65. Use browser interaction checks for any UI behavior that cannot be proven statically.
66. For canvas or 3D scenes, perform nonblank pixel checks and framing checks.
67. For responsive UI, test at least one narrow and one wide viewport or full-screen equivalent.
68. Check that visible text does not describe implementation details or keyboard shortcuts unless the product requires it.
69. Verify UI labels match backend payload names or localized copy where applicable.
70. Inspect visual hierarchy after data loads, not only in static mock states.

## F. Browser And Runtime Verification Upgrades

71. Start the local dev server when the app requires one and report the usable URL.
72. Reuse the repo's expected host and port for browser checks.
73. Snapshot or inspect the page before using element references.
74. Re-snapshot after navigation, modal opens, tab switches, or major DOM changes.
75. Capture artifacts into the repo's expected output directory.
76. Run at least one happy-path interaction for user-visible behavior.
77. Run at least one invalid or edge input when forms or actions are involved.
78. Verify API payloads after UI actions when frontend and backend must agree.
79. Check browser console errors when a UI appears visually wrong.
80. Verify loading and failure paths by forcing missing data or invalid inputs when feasible.
81. For game UI, verify state changes through both screen evidence and runtime state.
82. For asset-heavy UI, verify image loads, dimensions, and fallback behavior.
83. For routes, verify direct load and in-app navigation if both are supported.
84. For auth or external-service flows, stop at the credential boundary and report the exact blocker.
85. Prefer real browser evidence for visual claims over static code reading alone.

## G. Review Loop Upgrades

86. Run each requested review round as a distinct inspection pass.
87. In every round, try to find new issues instead of restating the previous pass.
88. Verify previous fixes still hold in later rounds.
89. If a fix is substantial, re-check affected adjacent areas.
90. Keep a short internal note per review round for the final report.
91. Separate code correctness review from product/UX review.
92. Separate runtime state review from visual screenshot review.
93. Include edge-case and invalid-input checks in at least one review round.
94. Include regression checks for neighboring features.
95. Include maintainability and unnecessary-complexity review before final.
96. Include documentation or usage consistency review when deliverables include docs or skills.
97. Treat passing tests as one evidence source, not as the entire review.
98. Mark unresolved issues explicitly instead of burying them under "known risks."
99. Do not claim a review round happened unless a fresh inspection was performed.
100. If a review finds issues, fix them and continue the remaining rounds afterward.

## H. Reporting And Memory Upgrades

101. Provide short progress reports during long work without dumping all internal reasoning.
102. After each completed work unit, report what changed, what was checked, and what remains.
103. Log discovered process, harness, permission, authentication, timeout, or instability issues before fixing them when repo rules require it.
104. Log the resolution separately with why it worked and how it was verified.
105. Use the user's requested final report format exactly when provided.
106. Include the total number of review rounds actually performed.
107. Include round-by-round summaries with findings and fixes.
108. Include bugs found at completion time, even if the answer is "none known after checks."
109. Include usage instructions for every major feature or function delivered.
110. State validations that could not be run and explain impact.

## I. Skill-Specific Upgrades

111. Keep `SKILL.md` concise and move large catalogs or examples into references.
112. Make trigger descriptions specific enough for implicit invocation.
113. Include relationship rules for adjacent skills to avoid workflow conflicts.
114. Add a quick-start path for normal use and an intensive path for high-risk use.
115. Add a completion audit rule that requires evidence per requirement.
116. Include examples only when they reduce ambiguity.
117. Avoid adding README, changelog, or auxiliary docs that the skill system does not need.
118. Add `agents/openai.yaml` with display name, short description, and default prompt.
119. Validate YAML frontmatter and metadata after editing.
120. Validate that references linked from `SKILL.md` exist.

## J. Practical Selection Heuristic

Pick improvements with this order:

1. Required by the user's instructions.
2. Required by repo or AGENTS.md rules.
3. Directly reduces a likely defect in the current task.
4. Produces objective evidence cheaply.
5. Improves future reuse without bloating `SKILL.md`.

Skip improvements that add ceremony without improving evidence, safety, or user-visible quality.
