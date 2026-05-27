# Build Monster Schema

## Context
Create the monster stat block JSON schema — the contract for all D&D 5e monster content files.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `.claude/skills/content/contracts/monster-schema.json`
- Full schema definition in `backlog/002-dnd-build-content-system/content-contracts.md` Contract 1
- Required fields: id, name, size_type, armor_class, hp, ability_scores, speed, challenge
- JSON Schema draft-07

## Acceptance Criteria
- [ ] `.claude/skills/content/contracts/monster-schema.json` exists
- [ ] File is valid JSON with `$schema` field

## Gates Satisfied
- BUILD-01, FUNC-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
