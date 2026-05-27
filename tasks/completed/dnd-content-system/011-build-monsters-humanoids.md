# Build Monster Files — Humanoids

## Context
Create Tier 3 monster files for humanoid enemies conforming to monster-schema.json.

## Type
BUILD

## Execution
inline

## Dependencies
- 001, 009

## Phase Gate
- [ ] `.claude/skills/content/contracts/monster-schema.json` exists
- [ ] `content/lost-mine-phandelver/manifest.json` exists

## Requirements
- Create `orc.json` — CR 1/2, AC 13, HP 15 (2d8+6), Medium
- Create `drow.json` — CR 1/4, AC 15, HP 13 (3d8), Medium
- Create `redbrand-ruffian.json` — CR 1/2, AC 12, HP 16 (3d8+3), Medium
- Create `redbrand-mage.json` — CR 2, AC 12, HP 22 (5d8), Medium, with spellcasting
- All in `content/lost-mine-phandelver/monsters/`

## Acceptance Criteria
- [ ] All 4 humanoid monster files exist with correct stats
- [ ] All files are valid JSON with required fields

## Gates Satisfied
- BUILD-10 (partial), FUNC-04, FUNC-07

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
