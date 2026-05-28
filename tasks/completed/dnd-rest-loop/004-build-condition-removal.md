# Build Condition Removal

## Context
Create condition_removal.py implementing condition removal rules for long/short rest.

## Type
BUILD

## Execution
inline

## Dependencies
- 001

## Requirements
- Create `.claude/skills/rest/condition_removal.py`
- `remove_conditions_long_rest(conditions)` — remove exhaustion, poisoned, stunned, charmed; keep blinded, frightened
- `remove_conditions_short_rest(conditions)` — no automatic condition removal on short rest
- `is_removable_by_long_rest(condition)` — returns bool for whether condition is removed by long rest
- Condition removal rules per rest-mechanics.md table

## Acceptance Criteria
- [ ] `.claude/skills/rest/condition_removal.py` exists
- [ ] `remove_conditions_long_rest` removes exhaustion, poisoned, stunned, charmed
- [ ] `remove_conditions_long_rest` keeps blinded, frightened
- [ ] `remove_conditions_short_rest` returns conditions unchanged

## Gates Satisfied
- BUILD-04, FUNC-04

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
