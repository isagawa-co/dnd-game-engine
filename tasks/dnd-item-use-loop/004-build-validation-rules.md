# Build Validation Rules

## Context
Create the validation-rules.json — defines all item usage validation checks.

## Type
BUILD

## Execution
inline

## Dependencies
- 001-build-item-use-contract

## Requirements
- Create `.claude/skills/item-use/contracts/validation-rules.json`
- Validation rules from backlog contract:
  - VAL-001: Item exists in inventory (quantity >= 1)
  - VAL-002: Item requirements met (attunement, level requirements)
  - VAL-003: Action available (action/bonus_action/reaction not already used)
  - VAL-004: No action conflict (can't use action if used for attack)
  - VAL-005: Target valid (alive, in party)
  - VAL-006: Effect applicable (healing on non-undead, no duplicate buffs)
- Each rule: rule_id, description, validation logic, error_code

## Acceptance Criteria
- [ ] `.claude/skills/item-use/contracts/validation-rules.json` exists
- [ ] File is valid JSON
- [ ] Contains 6 validation rules with rule IDs VAL-001 through VAL-006
- [ ] Each rule has error_code mapping to outcome codes

## Gates Satisfied
- BUILD-04, FUNC-04

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
