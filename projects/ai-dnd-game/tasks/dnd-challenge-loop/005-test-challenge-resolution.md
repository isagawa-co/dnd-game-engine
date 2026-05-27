# Test Challenge Resolution

## Context
Create test suite for challenge resolution module — verify DC determination, outcome classification, and consequence generation.

## Type
TEST

## Execution
inline

## Dependencies
- 003-build-challenge-resolution-py

## Requirements
- Create `.claude/skills/challenge/tests/test_challenge_resolution.py`
- Tests:
  - `test_determine_dc_moderate` — DC 12 for climb/moderate
  - `test_determine_dc_hard` — DC 15 for pick_lock/hard
  - `test_determine_dc_very_hard` — DC 18 for swim/very_hard
  - `test_determine_dc_investigate` — DC 10/13/16 for investigate
  - `test_outcome_code_success` — roll >= DC returns "success"
  - `test_outcome_code_partial_success` — roll DC-2 to DC-1 returns "partial_success"
  - `test_outcome_code_failure` — roll < DC-2 returns "failure"
  - `test_outcome_code_critical_failure` — natural 1 returns "critical_failure"
  - `test_consequence_climb_failure` — climb failure returns damage consequence
  - `test_consequence_pick_lock_failure` — pick_lock failure returns none consequence
  - `test_resolve_challenge_success` — full pipeline success path
  - `test_resolve_challenge_failure` — full pipeline failure path
- All tests must pass with `pytest`

## Acceptance Criteria
- [ ] `.claude/skills/challenge/tests/test_challenge_resolution.py` exists
- [ ] All 12 tests pass
- [ ] Tests cover all 4 outcome codes
- [ ] Tests cover DC determination for different types

## Gates Satisfied
- TEST-01, TEST-02

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
