# Test Item Validation Rules

## Context
Validate the validation-rules.json contains correct validation rule definitions.

## Type
TEST

## Execution
inline

## Dependencies
- 004-build-validation-rules

## Requirements
- Create `projects/ai-dnd-game/tests/test_item_validation.py`
- Test L1: validation rules file exists
- Test L2: file is valid JSON
- Test L3: contains 6 validation rules (VAL-001 through VAL-006)
- Test L3: each rule has rule_id, description, error_code
- Test L3: error codes map to correct outcome codes (item_not_found, attunement_required, action_blocked, target_invalid)
- Run with pytest, all tests must pass

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/tests/test_item_validation.py` exists
- [ ] Contains at least 4 test functions
- [ ] All tests pass with pytest

## Gates Satisfied
- TEST-03

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
