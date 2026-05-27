# Build Class Schema

## Context
Create the class definition JSON schema for D&D 5e classes.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `.claude/skills/content/contracts/class-schema.json`
- Full schema in `backlog/002-dnd-build-content-system/content-contracts.md` Contract 4
- Required fields: id, name, hit_die, proficiency_bonus_by_level

## Acceptance Criteria
- [ ] `.claude/skills/content/contracts/class-schema.json` exists
- [ ] File is valid JSON with `$schema` field

## Gates Satisfied
- BUILD-04, FUNC-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
