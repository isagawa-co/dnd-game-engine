# D&D Combat Loop — Task Index

## Goal
Build the combat loop sub-skill: initiative, round management, action resolution, damage/effects, and outcome contracts.

## Source
-> [[docs/backlog/010-dnd-build-combat-loop.md]]

## Tasks

| # | Task | Type | Dependencies | Status |
|---|------|------|-------------|--------|
| 001 | [[001-build-combat-loop-contract]] | BUILD | none | pending |
| 002 | [[002-build-combat-state-contract]] | BUILD | none | pending |
| 003 | [[003-build-combat-action-contract]] | BUILD | none | pending |
| 004 | [[004-build-combat-skill-md]] | BUILD | 001-003 | pending |
| 005 | [[005-test-validate-all-combat]] | TEST | 001-004 | pending |

## Gate Contract
-> [[gate-contract.md]]

## Deliverables
- `projects/ai-dnd-game/.claude/skills/combat/contracts/combat-loop-contract.json` — main combat loop contract
- `projects/ai-dnd-game/.claude/skills/combat/contracts/combat-state-contract.json` — combatant state contract
- `projects/ai-dnd-game/.claude/skills/combat/contracts/combat-action-contract.json` — action resolution contract
- `projects/ai-dnd-game/.claude/skills/combat/SKILL.md` — combat skill definition
