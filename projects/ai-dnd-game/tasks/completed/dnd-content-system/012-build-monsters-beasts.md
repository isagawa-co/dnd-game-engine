# Build Monster Files — Beasts & Vermin

## Context
Create Tier 3 monster files for beasts and vermin conforming to monster-schema.json.

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
- Create `owlbear.json` — CR 3, AC 13, HP 59 (7d10+21), Large
- Create `giant-spider.json` — CR 1, AC 14, HP 26 (4d10+4), Large
- Create `stirge.json` — CR 1/8, AC 14, HP 2 (1d4), Tiny
- Create `giant-rat.json` — CR 1/8, AC 12, HP 7 (2d6), Small
- Create `dire-wolf.json` — CR 1, AC 14, HP 37 (5d10+10), Large
- Create `black-bear.json` — CR 1/2, AC 11, HP 19 (3d8+6), Medium
- Create `rust-monster.json` — CR 1/2, AC 14, HP 27 (5d8+5), Medium
- All in `projects/ai-dnd-game/content/lost-mine-phandelver/monsters/`

## Acceptance Criteria
- [ ] All 7 beast/vermin monster files exist with correct stats
- [ ] All files are valid JSON with required fields

## Gates Satisfied
- BUILD-10 (partial), FUNC-04, FUNC-07

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
