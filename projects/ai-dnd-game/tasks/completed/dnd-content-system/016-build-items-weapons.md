# Build Item Files — Weapons

## Context
Create Tier 3 item files for weapons conforming to item-schema.json.

## Type
BUILD

## Execution
inline

## Dependencies
- 003, 009

## Phase Gate
- [ ] `projects/ai-dnd-game/.claude/skills/content/contracts/item-schema.json` exists
- [ ] `projects/ai-dnd-game/content/lost-mine-phandelver/manifest.json` exists

## Requirements
- Create `longsword.json` — weapon, common, 3 lb, 1d8 slashing, versatile
- Create `shortsword.json` — weapon, common, 2 lb, 1d6 piercing, finesse/light
- Create `crossbow.json` — weapon, common, 5 lb, 1d8 piercing, ammunition/loading/two-handed
- Create `dagger.json` — weapon, common, 1 lb, 1d4 piercing, finesse/light/thrown
- Create `club.json` — weapon, common, 2 lb, 1d4 bludgeoning, light
- Create `mace.json` — weapon, common, 4 lb, 1d6 bludgeoning
- Create `spear.json` — weapon, common, 3 lb, 1d6 piercing, thrown/versatile
- All in `projects/ai-dnd-game/content/lost-mine-phandelver/items/`

## Acceptance Criteria
- [ ] All 7 weapon files exist with correct damage stats
- [ ] All files are valid JSON with required fields

## Gates Satisfied
- BUILD-12 (partial), FUNC-06

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
