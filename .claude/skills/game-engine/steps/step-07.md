---
step: 7
name: Execute Build Pipeline
requires: ordered_backlog_items, gdd_context
produces: working_game_code, tests, req_coverage
---

# Step 7: Execute Build Pipeline

## Purpose

Build the game autonomously from the ordered backlog. Each system is built, tested, and verified against its REQ IDs before moving to the next. This step wraps `/kernel/execute-pipeline` with GDD-specific context.

## Input

- `backlog/NNN-system-name.md` — ordered backlog items from Step 6
- `docs/game-design/sections/*.md` — GDD sections for context
- `docs/game-design/profile.md` — platform/stack info
- `scripts/req-coverage` — coverage checker

## Actions

1. **Set GDD context** — configure execute-pipeline to pass relevant GDD section(s) as context for each task
2. **For each backlog item** (in dependency order):
   a. Read the backlog item and its referenced GDD section(s)
   b. Invoke execute-pipeline with the backlog item
   c. Execute-pipeline decomposes into atomic tasks and runs via `run-task.sh`
   d. After completion: run tests for this system
   e. Verify REQ IDs are covered (test names include REQ IDs)
   f. Run coverage script for progressive coverage
3. **After all systems built:**
   a. Run full test suite
   b. Run final coverage report
   c. Generate build summary

## Output

- Source code in `src/` (or platform-appropriate directory)
- Tests in `tests/` with REQ IDs in function names
- Coverage report from coverage script
- Build state updated with completed systems

## Verification

- [ ] Each system has source files and test files
- [ ] Test names include REQ IDs
- [ ] Full test suite passes
- [ ] Coverage script shows 100% REQ coverage (no orphans)
- [ ] No hardcoded balance values in source (config only)
- [ ] All build gates from gate-contract.md pass

## Failure Modes

| Failure | Symptom | Recovery |
|---------|---------|----------|
| Test failure on REQ | `pytest` fails for specific REQ | Read GDD section for exact spec, fix implementation to match |
| Import errors | Module not found | Check dependency order, ensure prerequisite systems are built |
| Coverage gap | REQ with no test | Write test for uncovered REQ, re-run coverage |
| External dep missing | Package not installed | Check `docs/game-design/sections/NN-external-deps.md`, install |

## Example

**Building combat system (backlog item 005):**

1. Read `backlog/005-combat.md` → REQ-COMBAT-001 through REQ-COMBAT-008
2. Read `docs/game-design/sections/05-rules-mechanics.md` for exact formulas
3. Execute-pipeline generates:
   - Combat skill contracts — damage calculation, modifiers, resolution
   - Combat gate contract — one gate per REQ ID
4. Run combat loop verification → all gates pass
5. Run coverage → 005 system at 100%
