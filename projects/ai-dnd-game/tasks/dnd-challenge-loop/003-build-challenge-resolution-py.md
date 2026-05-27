# Build Challenge Resolution Module

## Context
Create the Python module that resolves challenge encounters: determines DC, makes ability checks, computes outcome code, applies consequences.

## Type
BUILD

## Execution
inline

## Dependencies
- 001-build-challenge-action-contract
- 002-build-challenge-outcome-contract

## Requirements
- Create `.claude/skills/challenge/challenge_resolution.py`
- Functions:
  - `determine_dc(challenge_type, difficulty)` — returns DC value based on type and difficulty tier (moderate/hard/very_hard)
  - `resolve_challenge(action)` — takes challenge action dict, computes outcome dict per contracts
  - `compute_outcome_code(roll_total, dc)` — returns result_code (success/partial_success/failure/critical_failure)
  - `compute_consequence(challenge_type, result_code, margin)` — returns consequence dict (type, damage_amount, etc.)
- Uses `atomic_ops.check_operations.ability_check` for the underlying d20 check
- DC mapping from design doc: moderate=12, hard=15, very_hard=18 (investigate: 10/13/16)
- Outcome codes: success (>= DC), partial_success (DC-2 to DC-1), failure (< DC-2), critical_failure (natural 1)
- Consequence rules from design doc (climb=fall damage, swim=exhaustion, etc.)

## Acceptance Criteria
- [ ] `.claude/skills/challenge/challenge_resolution.py` exists
- [ ] `determine_dc` returns correct DC for each challenge type + difficulty combo
- [ ] `resolve_challenge` returns a valid outcome dict matching outcome contract
- [ ] `compute_outcome_code` correctly classifies all 4 result codes
- [ ] `compute_consequence` returns appropriate consequence per challenge type and result code
- [ ] Module imports `ability_check` from atomic_ops

## Gates Satisfied
- FUNC-01, FUNC-02, FUNC-03

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
