# Build Monster Files — Undead & Remaining

## Context
Create remaining Tier 3 monster files to reach 24 total.

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
- Create `zombie.json` — CR 1/4, AC 8, HP 22 (3d8+9), Medium, undead
- Create `skeleton.json` — CR 1/4, AC 13, HP 13 (2d8+4), Medium, undead
- Verify total monster count reaches 24 across tasks 010-014
- Add any remaining monsters from manifest if count < 24
- All in `content/lost-mine-phandelver/monsters/`

## Acceptance Criteria
- [ ] `zombie.json` and `skeleton.json` exist with correct stats
- [ ] Total monster files in `monsters/` directory equals 24
- [ ] All files are valid JSON with required fields

## Gates Satisfied
- BUILD-10, FUNC-04, FUNC-07

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
