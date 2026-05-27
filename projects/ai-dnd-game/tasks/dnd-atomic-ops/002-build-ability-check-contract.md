# Task 002: Build Ability Check Contract

## Action
Write `.claude/skills/atomic-ops/contracts/ability-check-contract.json`

## Source
`docs/backlog/003-dnd-build-atomic-ops/check-operations.md`

## Deliverable
JSON contract file with:
- Input schema: ability_score (3-20), proficiency (0,2-6), dc (5-30), advantage (bool), disadvantage (bool)
- Output schema: roll (1-20), ability_mod (-4 to 5), proficiency_bonus (0-6), total (-3 to 31), dc, success (bool)
- Validation rules: CHECK-001 through CHECK-004

## Acceptance Criteria
- [ ] File exists at `.claude/skills/atomic-ops/contracts/ability-check-contract.json`
- [ ] Valid JSON with input_schema, output_schema, validation_rules
- [ ] All 4 CHECK rules present
- [ ] Ability modifier formula documented: (ability_score - 10) / 2 floor
