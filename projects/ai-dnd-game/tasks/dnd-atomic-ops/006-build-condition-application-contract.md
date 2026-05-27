# Task 006: Build Condition Application Contract

## Action
Write `.claude/skills/atomic-ops/contracts/condition-application-contract.json`

## Source
`docs/backlog/003-dnd-build-atomic-ops/effect-operations.md`

## Deliverable
JSON contract file with:
- Input schema: entity_id, entity_condition_immunities, entity_current_conditions, entity_concentrating, condition_to_apply (with stacking mode), source_spell_or_effect
- Output schema: success, reason (applied/immune/invalid), condition_immune, concentration_lost, entity_conditions_after
- Validation rules: COND-001 through COND-006

## Acceptance Criteria
- [ ] File exists at `.claude/skills/atomic-ops/contracts/condition-application-contract.json`
- [ ] Valid JSON with input_schema, output_schema, validation_rules
- [ ] All 6 COND rules present
- [ ] Three stacking modes documented (no_stack, stack, replace)
