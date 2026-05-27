# Test Validate All Combat Contracts

## Context
Validate all combat skill deliverables: JSON schemas are valid, SKILL.md exists and references all contracts.

## Type
TEST

## Execution
inline

## Dependencies
- 001-build-combat-loop-contract
- 002-build-combat-state-contract
- 003-build-combat-action-contract
- 004-build-combat-skill-md

## Requirements
- Validate all 3 JSON contract files are valid JSON with $schema field
- Validate SKILL.md exists and contains references to all 3 contracts
- Validate combat-loop-contract.json has combat_input and combat_outcome definitions
- Validate combat-state-contract.json has combatant_state and round_state definitions
- Validate combat-action-contract.json has action_request and action_result definitions
- Run validation via python3 json.loads() and file existence checks

## Acceptance Criteria
- [ ] All 3 JSON files parse as valid JSON
- [ ] All 3 JSON files have `$schema` field
- [ ] SKILL.md references all 3 contracts
- [ ] All files exist at correct paths under `projects/ai-dnd-game/.claude/skills/combat/`

## Gates Satisfied
- TEST-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
