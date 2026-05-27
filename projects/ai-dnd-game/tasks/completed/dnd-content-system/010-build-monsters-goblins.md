# Build Monster Files — Goblinoids

## Context
Create Tier 3 monster files for goblinoid creatures conforming to monster-schema.json.

## Type
BUILD

## Execution
inline

## Dependencies
- 001, 009

## Phase Gate
- [ ] `projects/ai-dnd-game/.claude/skills/content/contracts/monster-schema.json` exists
- [ ] `projects/ai-dnd-game/content/lost-mine-phandelver/manifest.json` exists

## Requirements
- Create `projects/ai-dnd-game/content/lost-mine-phandelver/monsters/goblin.json` — CR 1/4, AC 15, HP 7 (2d6), Small
- Create `projects/ai-dnd-game/content/lost-mine-phandelver/monsters/hobgoblin.json` — CR 1/2, AC 18, HP 11 (2d8+2), Medium
- Create `projects/ai-dnd-game/content/lost-mine-phandelver/monsters/bugbear.json` — CR 1, AC 16, HP 27 (5d8+5), Medium
- Schema example in `projects/ai-dnd-game/backlog/002-dnd-build-content-system/pack-structure.md`

## Acceptance Criteria
- [ ] All 3 goblinoid monster files exist with correct AC/HP/CR
- [ ] All files are valid JSON with required fields

## Gates Satisfied
- BUILD-10 (partial), FUNC-04, FUNC-07

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
