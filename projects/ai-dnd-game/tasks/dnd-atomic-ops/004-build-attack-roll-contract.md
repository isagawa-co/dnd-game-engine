# Task 004: Build Attack Roll Contract

## Action
Write `.claude/skills/atomic-ops/contracts/attack-roll-contract.json`

## Source
`docs/backlog/003-dnd-build-atomic-ops/attack-operations.md`

## Deliverable
JSON contract file with:
- Input schema: attack_bonus (-5 to +20), target_ac (1-30), advantage (bool), disadvantage (bool)
- Output schema: roll (1-20), attack_bonus, total (-4 to 40), target_ac, hit (bool), critical_hit (bool), critical_miss (bool)
- Validation rules: ATTACK-001 through ATTACK-005

## Acceptance Criteria
- [ ] File exists at `.claude/skills/atomic-ops/contracts/attack-roll-contract.json`
- [ ] Valid JSON with input_schema, output_schema, validation_rules
- [ ] All 5 ATTACK rules present
- [ ] Natural 20 always hits, natural 1 always misses documented
