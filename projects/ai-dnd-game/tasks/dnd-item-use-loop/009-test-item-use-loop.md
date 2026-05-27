# Test Item-Use Loop Integration

## Context
Integration test validating the complete item-use skill: SKILL.md references valid contracts, all contracts cross-reference correctly.

## Type
TEST

## Execution
inline

## Dependencies
- 005-build-item-use-skill

## Requirements
- Create `projects/ai-dnd-game/tests/test_item_use_loop.py`
- Test L1: SKILL.md exists
- Test L2: all 4 contract files referenced in SKILL.md exist
- Test L3: item-use-loop-contract output result_codes match validation-rules error_codes
- Test L3: item-effect-catalog item types match contract item_type enum
- Test L3: attunement-rules rule count matches SKILL.md description
- Run with pytest, all tests must pass

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/tests/test_item_use_loop.py` exists
- [ ] Contains at least 5 test functions
- [ ] All tests pass with pytest

## Gates Satisfied
- TEST-04

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
