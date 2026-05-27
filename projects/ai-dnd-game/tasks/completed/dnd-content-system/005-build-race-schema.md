# Build Race Schema

## Context
Create the race definition JSON schema for D&D 5e races.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `projects/ai-dnd-game/.claude/skills/content/contracts/race-schema.json`
- Full schema in `projects/ai-dnd-game/backlog/002-dnd-build-content-system/content-contracts.md` Contract 5
- Required fields: id, name, ability_score_increases, size, speed

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/.claude/skills/content/contracts/race-schema.json` exists
- [ ] File is valid JSON with `$schema` field

## Gates Satisfied
- BUILD-05, FUNC-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
