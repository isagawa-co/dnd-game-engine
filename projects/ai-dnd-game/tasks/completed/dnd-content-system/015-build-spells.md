# Build Spell Files

## Context
Create Tier 3 spell files for Lost Mine of Phandelver conforming to spell-schema.json.

## Type
BUILD

## Execution
inline

## Dependencies
- 002, 009

## Phase Gate
- [ ] `projects/ai-dnd-game/.claude/skills/content/contracts/spell-schema.json` exists
- [ ] `projects/ai-dnd-game/content/lost-mine-phandelver/manifest.json` exists

## Requirements
- Create `magic-missile.json` — 1st level evocation, V/S, 120ft, instantaneous, 1d4+1 force
- Create `scorching-ray.json` — 2nd level evocation, V/S, 120ft, instantaneous, 2d6 fire
- Create `hold-person.json` — 2nd level enchantment, V/S/M, 60ft, concentration 1 min, Wisdom save
- All in `projects/ai-dnd-game/content/lost-mine-phandelver/spells/`

## Acceptance Criteria
- [ ] All 3 spell files exist with correct level and school
- [ ] All files are valid JSON with required fields

## Gates Satisfied
- BUILD-11, FUNC-05

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
