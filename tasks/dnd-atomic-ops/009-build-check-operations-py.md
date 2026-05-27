# Task 009: Build Check Operations Implementation

## Action
Write `.claude/skills/atomic-ops/operations/check_operations.py`

## Source
`docs/backlog/003-dnd-build-atomic-ops/check-operations.md`

## Deliverable
Python implementation of:
- `ability_check(ability_score, proficiency, dc, advantage, disadvantage)`
- `saving_throw(ability_score, proficiency, dc, advantage, disadvantage)`

Both validate against check contracts and return matching output.

## Acceptance Criteria
- [ ] File exists at `.claude/skills/atomic-ops/operations/check_operations.py`
- [ ] Both functions accept correct parameters
- [ ] Validates inputs (ability_score 3-20, proficiency valid, dc 5-30)
- [ ] Returns dict matching output schema
- [ ] Ability modifier: (ability_score - 10) // 2
