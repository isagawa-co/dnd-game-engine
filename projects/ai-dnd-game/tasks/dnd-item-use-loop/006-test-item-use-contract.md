# Test Item-Use Contract

## Context
Validate the item-use-loop-contract.json is valid JSON Schema and covers all required fields.

## Type
TEST

## Execution
inline

## Dependencies
- 001-build-item-use-contract

## Requirements
- Create `projects/ai-dnd-game/tests/test_item_use_contract.py`
- Test L1: contract file exists
- Test L2: file is valid JSON, has $schema field
- Test L3: input schema has required fields (action_type, actor_pc, target_pc, item_id, item_type, action_cost)
- Test L3: output schema has required fields (success, result_code, effect_applied, state_mutations)
- Test L3: result_code enum contains all 5 outcome codes
- Run with pytest, all tests must pass

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/tests/test_item_use_contract.py` exists
- [ ] Contains at least 5 test functions
- [ ] All tests pass with pytest

## Gates Satisfied
- TEST-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
