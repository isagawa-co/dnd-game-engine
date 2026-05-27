# Build Spell Schema

## Context
Create the spell definition JSON schema for all D&D 5e spells.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `.claude/skills/content/contracts/spell-schema.json`
- Full schema in `backlog/002-dnd-build-content-system/content-contracts.md` Contract 2
- Required fields: id, name, level, school, casting_time, range, components, duration, description

## Acceptance Criteria
- [ ] `.claude/skills/content/contracts/spell-schema.json` exists
- [ ] File is valid JSON with `$schema` field

## Gates Satisfied
- BUILD-02, FUNC-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
