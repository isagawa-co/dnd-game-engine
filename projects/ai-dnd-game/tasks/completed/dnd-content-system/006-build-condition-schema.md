# Build Condition Schema

## Context
Create the condition definition JSON schema for D&D 5e conditions.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `projects/ai-dnd-game/.claude/skills/content/contracts/condition-schema.json`
- Full schema in `projects/ai-dnd-game/backlog/002-dnd-build-content-system/content-contracts.md` Contract 6
- Required fields: id, name, description, effects

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/.claude/skills/content/contracts/condition-schema.json` exists
- [ ] File is valid JSON with `$schema` field

## Gates Satisfied
- BUILD-06, FUNC-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
