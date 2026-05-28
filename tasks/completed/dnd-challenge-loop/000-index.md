# D&D Challenge Loop — Task Index

## Goal
Build challenge loop sub-skill that resolves environmental obstacles and skill challenges: parse challenge type, make ability checks vs DC, apply success/failure consequences, return outcome to scene loop.

## Source
→ [[docs/backlog/012-dnd-build-challenge-loop.md]]

## Tasks

| # | Task | Type | Dependencies | Status |
|---|------|------|-------------|--------|
| 001 | [[001-build-challenge-action-contract]] | BUILD | none | pending |
| 002 | [[002-build-challenge-outcome-contract]] | BUILD | none | pending |
| 003 | [[003-build-challenge-resolution-py]] | BUILD | 001, 002 | pending |
| 004 | [[004-build-challenge-skill-md]] | BUILD | 001-003 | pending |
| 005 | [[005-test-challenge-resolution]] | TEST | 003 | pending |

## Gate Contract
→ [[gate-contract.md]]

## Deliverables
- `.claude/skills/challenge/contracts/challenge-action-contract.json` — Input contract
- `.claude/skills/challenge/contracts/challenge-outcome-contract.json` — Output contract
- `.claude/skills/challenge/challenge_resolution.py` — Resolution module
- `.claude/skills/challenge/SKILL.md` — Challenge orchestrator skill
- `.claude/skills/challenge/tests/test_challenge_resolution.py` — Tests
