# Task 010: Build Attack Roll Implementation

## Action
Write `.claude/skills/atomic-ops/operations/attack_roll.py`

## Source
`docs/backlog/003-dnd-build-atomic-ops/attack-operations.md`

## Deliverable
Python implementation of `attack_roll(attack_bonus, target_ac, advantage, disadvantage)`.

## Acceptance Criteria
- [ ] File exists at `.claude/skills/atomic-ops/operations/attack_roll.py`
- [ ] Validates inputs (attack_bonus -5 to +20, target_ac 1-30)
- [ ] Natural 20 always hits (critical_hit=true)
- [ ] Natural 1 always misses (critical_miss=true)
- [ ] Returns dict matching output schema
