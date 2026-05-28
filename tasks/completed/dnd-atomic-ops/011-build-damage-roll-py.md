# Task 011: Build Damage Roll Implementation

## Action
Write `.claude/skills/atomic-ops/operations/damage_roll.py`

## Source
`docs/backlog/003-dnd-build-atomic-ops/damage-operations.md`

## Deliverable
Python implementation of `damage_roll(damage_dice, damage_type, target_resistances, target_immunities, target_vulnerabilities)`.

## Acceptance Criteria
- [ ] File exists at `.claude/skills/atomic-ops/operations/damage_roll.py`
- [ ] Parses XdY+Z dice format
- [ ] Resistance halves (floor), immunity zeroes, vulnerability doubles
- [ ] Immunity takes precedence over vulnerability
- [ ] Returns dict matching output schema
