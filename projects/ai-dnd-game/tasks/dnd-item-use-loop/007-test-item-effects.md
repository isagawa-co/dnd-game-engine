# Test Item Effects

## Context
Validate the item-effect-catalog.json contains correct item definitions.

## Type
TEST

## Execution
inline

## Dependencies
- 002-build-item-effect-catalog

## Requirements
- Create `projects/ai-dnd-game/tests/test_item_effects.py`
- Test L1: catalog file exists
- Test L2: file is valid JSON
- Test L3: contains at least 8 items
- Test L3: potion_healing has correct effect (restore_hp, amount 1d4+4, consumed=true)
- Test L3: equipment items have consumed=false
- Test L3: all items have required fields (id, name, effect, duration, consumed)
- Run with pytest, all tests must pass

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/tests/test_item_effects.py` exists
- [ ] Contains at least 5 test functions
- [ ] All tests pass with pytest

## Gates Satisfied
- TEST-02

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
