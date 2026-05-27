# Task 005: Build Damage Roll Contract

## Action
Write `.claude/skills/atomic-ops/contracts/damage-roll-contract.json`

## Source
`docs/backlog/003-dnd-build-atomic-ops/damage-operations.md`

## Deliverable
JSON contract file with:
- Input schema: damage_dice (XdY+Z pattern), damage_type (13 types), target_resistances, target_immunities, target_vulnerabilities (arrays)
- Output schema: damage_dice, rolled_damage, damage_type, is_resistant, is_immune, is_vulnerable, final_damage
- Validation rules: DMG-001 through DMG-007

## Acceptance Criteria
- [ ] File exists at `.claude/skills/atomic-ops/contracts/damage-roll-contract.json`
- [ ] Valid JSON with input_schema, output_schema, validation_rules
- [ ] All 7 DMG rules present
- [ ] Immunity precedence over vulnerability documented (DMG-007)
