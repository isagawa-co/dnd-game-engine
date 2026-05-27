# Build Catalog JSON (Tier 1)

## Context
Create the master content catalog — Tier 1. Lists all available content packs. Loaded once per campaign session.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `projects/ai-dnd-game/.claude/skills/content/catalog.json`
- Spec in `projects/ai-dnd-game/backlog/002-dnd-build-content-system/content-tiers.md` Tier 1
- Must contain Lost Mine of Phandelver entry: id, name, version 1.0.0, manifest_path, content_count, tier_loading eager

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/.claude/skills/content/catalog.json` exists
- [ ] File is valid JSON with packs array containing Lost Mine entry

## Gates Satisfied
- BUILD-07, FUNC-02

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
