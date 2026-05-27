# Task 001: Build Dice Roll Contract

## Action
Write `.claude/skills/atomic-ops/contracts/dice-roll-contract.json`

## Source
`docs/backlog/003-dnd-build-atomic-ops/dice-operations.md`

## Deliverable
JSON contract file with:
- Input schema: advantage (bool), disadvantage (bool), modifier (int -5 to +20)
- Output schema: die_rolls (array 1-2), selected_roll (1-20), modifier, total (-4 to 40), critical (bool), critical_fail (bool)
- Validation rules: DICE-001 (no both adv/disadv), DICE-002 (modifier range), DICE-003 (cancel logic)

## Acceptance Criteria
- [ ] File exists at `.claude/skills/atomic-ops/contracts/dice-roll-contract.json`
- [ ] Valid JSON with $schema, input_schema, output_schema, validation_rules sections
- [ ] Input schema matches design doc exactly
- [ ] Output schema matches design doc exactly
- [ ] All 3 validation rules present (DICE-001, DICE-002, DICE-003)
- [ ] File validates as JSON (no syntax errors)
