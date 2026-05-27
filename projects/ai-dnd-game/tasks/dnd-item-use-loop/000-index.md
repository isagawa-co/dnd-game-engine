# D&D Item-Use Loop — Task Index

## Goal
Build the item-use sub-loop skill: validate item possession, apply item effects (healing, buff, equipment), consume consumables, update inventory and PC state.

## Source
→ [[projects/ai-dnd-game/backlog/016-dnd-build-item-use-loop.md]]
→ [[projects/ai-dnd-game/backlog/016-dnd-build-item-use-loop/item-effect-contract.md]]

## Tasks

| # | Task | Type | Dependencies | Status |
|---|------|------|-------------|--------|
| 001 | [[001-build-item-use-contract]] | BUILD | none | pending |
| 002 | [[002-build-item-effect-catalog]] | BUILD | none | pending |
| 003 | [[003-build-attunement-rules]] | BUILD | none | pending |
| 004 | [[004-build-validation-rules]] | BUILD | 001 | pending |
| 005 | [[005-build-item-use-skill]] | BUILD | 001-004 | pending |
| 006 | [[006-test-item-use-contract]] | TEST | 001 | pending |
| 007 | [[007-test-item-effects]] | TEST | 002 | pending |
| 008 | [[008-test-item-validation]] | TEST | 004 | pending |
| 009 | [[009-test-item-use-loop]] | TEST | 005 | pending |

## Gate Contract
→ [[gate-contract.md]]

## Deliverables
- `projects/ai-dnd-game/.claude/skills/item-use/SKILL.md` — skill definition
- `projects/ai-dnd-game/.claude/skills/item-use/contracts/item-use-loop-contract.json` — input/output contract
- `projects/ai-dnd-game/.claude/skills/item-use/contracts/item-effect-catalog.json` — effect catalog
- `projects/ai-dnd-game/.claude/skills/item-use/contracts/attunement-rules.json` — attunement rules
- `projects/ai-dnd-game/.claude/skills/item-use/contracts/validation-rules.json` — validation rules
