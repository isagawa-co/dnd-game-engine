# Campaign Loop — Contract-Driven Redesign

## Status
EXISTS — needs refactor (remove Python code, add contracts)

## Location
`.claude/skills/campaign/` (remove campaign-loop.py, arc-transition.py, state-manager.py; add 4 contracts)

## What

Campaign loop currently has SKILL.md + 3 Python files (campaign-loop.py, arc-transition.py, state-manager.py). Must remove Python orchestration code and replace with pure contracts defining arc progression, state mutations, phase transitions, and completion rules. Campaign loop orchestrates campaign phases: load → resume → play scenes → check arc completion → save → exit.

## Current State

- campaign/SKILL.md (240 lines) ✓ exists
- campaign-loop.py — orchestration logic (must remove)
- arc-transition.py — arc progression rules (must remove)
- state-manager.py — state mutation logic (must remove)
- NO contracts ✗

## Deliverables

1. **campaign/SKILL.md** (refactor) — remove references to Python files, add contract references
2. **campaign/contracts/campaign-action-contract.json** — input from game-session: campaign_id, iteration count
3. **campaign/contracts/campaign-outcome-contract.json** — output: phase completion, arc transition, state mutations
4. **campaign/contracts/arc-progression-contract.json** — rules for arc completion (encounter threshold, story beats, plot flags)
5. **campaign/contracts/state-mutation-contract.json** — atomic state changes to campaign/arc/session/scene tiers
6. **campaign/workflow.md** (reference) — how campaign loop executes phases via contracts

## Dependencies

- Depends on: game-session (load/save), scene-loop (play scenes), state-evaluation-contract (routing)
- Sub-loops return outcomes that campaign applies to state

## Integration Point

Game-play command → campaign-loop (orchestrates phases) → scene-loop (per scene) → update state per outcomes

Campaign loop validates:
- Incoming campaign_action matches campaign-action-contract
- Arc completion per arc-progression-contract rules
- State mutations match state-mutation-contract schema
- Output matches campaign-outcome-contract

## Anti-Pattern: No Python Code

Remove all orchestration logic from Python. Contracts define rules. Orchestrator (game-play command or campaign-session skill) applies them.
