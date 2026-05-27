---
name: game-build
type: command
domain: game-engine
kernel_loop: true
---

# /game-build

Decompose a completed GDD into systems and build the game autonomously.

## Kernel Loop Integration

```
/kernel/anchor -> this command -> /kernel/complete
```

## Instructions

1. **Read skill files:**
   - `.claude/skills/game-engine/SKILL.md`
   - `.claude/skills/game-engine/workflow.md`
   - `.claude/skills/game-engine/gate-contract.md`

2. **Run Phase Transition Gate (Step 5):**
   - Read `steps/step-05.md`
   - Verify GDD completeness (all sections, all REQ IDs, profile approved)
   - If FAIL: report what's missing, direct user to `/game-create`

3. **Decompose GDD (Step 6):**
   - Read `steps/step-06.md`
   - Identify systems, build dependency graph, generate ordered backlog

4. **Execute Build Pipeline (Step 7):**
   - Read `steps/step-07.md`
   - For each backlog item: invoke execute-pipeline with GDD context
   - Run tests after each system
   - Run coverage check progressively

5. **On failure:**
   - Read `steps/on-failure.md` for diagnosis
   - Fix → `/kernel/learn` → retry (max 3)

6. **On completion:**
   - Run final test suite + coverage report
   - Report: "Game built — N systems, M tests, 100% REQ coverage."
   - `/kernel/complete`

## Usage

```
/game-build
```

Requires a completed GDD from `/game-create`. No arguments needed — reads GDD from `docs/game-design/`.
