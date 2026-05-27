# Task Atomicity — Lesson Detail

## Rule
One task = one action = one file. If a task touches N files, create N tasks. No bundling, no grouping, no "related work" exceptions.

## Recurrence Log

### 2026-03-23 — Original violation (3x in one session)
- **Issue:** Agent bundled 3-10 actions into single tasks
- **Root cause:** "merge if <3" rule in task-builder skill
- **Fix:** Removed the merge rule. User corrected 3 times.

### 2026-04-28 — Recurrence: 53-man rosters division grouping
- **Issue:** Agent grouped 4 teams per task (by NFL division) instead of 1 team per task. Task-builder SKILL.md step-06 explicitly says "if it touches N files, it's N tasks" and "NEVER bundle multiple file writes into one task."
- **Root cause:** Agent rationalized that "4 teams in the same division IS related" and that "32 separate tasks would be extremely slow execution." Both are improvised justifications that override the written rule.
- **Impact:** Sub-agents running 4-team tasks ran out of context, produced partial results, emitted ALL_TASKS_COMPLETE prematurely, required multiple re-launches. Individual team tasks would have completed reliably.
- **Fix:** Should have created 32 individual team tasks + validation tasks = 33+ tasks. The "execution speed" concern is irrelevant — correctness beats speed.
- **Pattern:** Agent reads rule → invents exception → bundles → context blowout → user catches it. Same pattern as original violation.

## Anti-Pattern
"These are related, so I'll group them" — No. Related actions that touch different files are STILL separate tasks. The relationship makes them sequential or parallel, not bundled.

## Quality Gate
Before writing task files, count the number of files that will be modified. If task count < file count, the decomposition is wrong.
