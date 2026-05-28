# Build Interruption Mechanics

## Context
Create interruption.py implementing location safety and rest interruption logic.

## Type
BUILD

## Execution
inline

## Dependencies
- 001

## Requirements
- Create `.claude/skills/rest/interruption.py`
- `check_interruption(location_safety, rng=None)` — roll for interruption based on location safety
- `get_location_cost(location_safety)` — return gold cost for resting at location
- Location safety table: safe_inn=0%, adventurers_guild=5%, camp_fire=20%, dangerous_area=50%
- Returns dict with interrupted (bool), cost_gold (int)

## Acceptance Criteria
- [ ] `.claude/skills/rest/interruption.py` exists
- [ ] `check_interruption` returns correct interruption chance per location
- [ ] `get_location_cost` returns correct gold cost per location
- [ ] safe_inn always returns interrupted=False

## Gates Satisfied
- BUILD-05, FUNC-05

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
