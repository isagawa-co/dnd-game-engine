# Build Rest Tests

## Context
Create test_rest.py with L1/L2/L3 tests for all rest operations.

## Type
TEST

## Execution
inline

## Dependencies
- 003, 004, 005

## Requirements
- Create `.claude/skills/rest/tests/test_rest.py`
- L1: All modules import without error
- L2: All functions run with valid inputs, return expected types
- L3: Correct results on real scenarios (long rest full recovery, short rest partial recovery, hit die roll, condition removal, interruption)
- Minimum 10 test functions

## Acceptance Criteria
- [ ] `.claude/skills/rest/tests/test_rest.py` exists
- [ ] All tests pass with `pytest`
- [ ] Minimum 10 test functions
- [ ] Covers long rest, short rest, hit die, conditions, interruption

## Gates Satisfied
- TEST-01, TEST-02, TEST-03

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
