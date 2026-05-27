# Build Monster Files — Named NPCs

## Context
Create Tier 3 monster files for named NPCs and bosses with custom stat blocks.

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
- Create `king-grol.json` — CR 3, Bugbear king, AC 16, HP 45
- Create `king-grol-officers.json` — CR 1, Bugbear officers, AC 16, HP 27
- Create `sildar-hallwinter.json` — CR 1, Human veteran, AC 16, HP 27
- Create `iarno-albrek.json` — CR 2, Wizard (Glasstaff), AC 12, HP 22, spellcasting
- Create `gundren-rockseeker.json` — CR 0, Dwarf NPC, AC 10, HP 11
- Create `nothic.json` — CR 2, Aberration, AC 15, HP 45 (6d8+18)
- All in `content/lost-mine-phandelver/monsters/`

## Acceptance Criteria
- [ ] All 6 NPC/boss monster files exist with correct stats
- [ ] All files are valid JSON with required fields

## Gates Satisfied
- BUILD-10 (partial), FUNC-04, FUNC-07

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
