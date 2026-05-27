# Build Item Schema

## Context
Create the item definition JSON schema for weapons, armor, potions, magical items.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `.claude/skills/content/contracts/item-schema.json`
- Full schema in `backlog/002-dnd-build-content-system/content-contracts.md` Contract 3
- Required fields: id, name, type, rarity

## Acceptance Criteria
- [ ] `.claude/skills/content/contracts/item-schema.json` exists
- [ ] File is valid JSON with `$schema` field

## Gates Satisfied
- BUILD-03, FUNC-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
