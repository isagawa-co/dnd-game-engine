# Task 008: Build Dice Roll Implementation

## Action
Write `.claude/skills/atomic-ops/operations/dice_roll.py`

## Source
`docs/backlog/003-dnd-build-atomic-ops/dice-operations.md` (Reference Implementation Logic)

## Deliverable
Python implementation of `dice_roll(advantage, disadvantage, modifier)` that:
- Validates inputs against dice-roll-contract.json input schema
- Executes d20 roll logic (advantage/disadvantage selection)
- Returns output matching dice-roll-contract.json output schema
- Pure function, no side effects

## Acceptance Criteria
- [ ] File exists at `.claude/skills/atomic-ops/operations/dice_roll.py`
- [ ] `dice_roll()` function accepts advantage, disadvantage, modifier
- [ ] Validates inputs (rejects both adv+disadv, modifier out of range)
- [ ] Returns dict matching output schema
- [ ] Imports and runs without errors
