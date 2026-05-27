# Task 013: Test Dice Operations

## Action
Write and run `projects/ai-dnd-game/tests/test_dice_operations.py`

## Source
`docs/backlog/003-dnd-build-atomic-ops/dice-operations.md` (Acceptance Criteria: 20+ tests)

## Deliverable
Pytest file with 20+ tests covering:
- Normal roll (no advantage/disadvantage)
- Advantage (rolls 2d20, takes higher)
- Disadvantage (rolls 2d20, takes lower)
- Critical (natural 20)
- Critical fail (natural 1)
- Extreme modifiers (-5, +20)
- Validation rejects both adv+disadv true
- Output schema compliance

## Acceptance Criteria
- [ ] Test file exists
- [ ] 20+ test functions
- [ ] All tests pass
- [ ] Covers all scenarios from design doc
