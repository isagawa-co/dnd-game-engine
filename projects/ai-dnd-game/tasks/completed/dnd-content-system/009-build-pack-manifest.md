# Build Pack Manifest (Tier 2)

## Context
Create the Lost Mine of Phandelver manifest — Tier 2. Lists all content with wiki-link paths.

## Type
BUILD

## Execution
inline

## Dependencies
- 007

## Phase Gate
- [ ] `projects/ai-dnd-game/.claude/skills/content/catalog.json` exists

## Requirements
- Create `projects/ai-dnd-game/content/lost-mine-phandelver/manifest.json`
- Must contain: pack_id, version, monsters (24), spells (3), items (18), classes ([]), races ([]), conditions ([])
- Wiki-link format: `content:lost-mine-phandelver/[type]/[id]`
- Full lists in `projects/ai-dnd-game/backlog/002-dnd-build-content-system/pack-structure.md`

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/content/lost-mine-phandelver/manifest.json` exists
- [ ] monsters array has 24 entries, spells 3, items 18

## Gates Satisfied
- BUILD-09, FUNC-03, FUNC-08

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
