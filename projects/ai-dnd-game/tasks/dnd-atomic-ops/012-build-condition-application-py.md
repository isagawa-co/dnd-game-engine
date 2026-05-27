# Task 012: Build Condition Application Implementation

## Action
Write `.claude/skills/atomic-ops/operations/condition_application.py`

## Source
`docs/backlog/003-dnd-build-atomic-ops/effect-operations.md`

## Deliverable
Python implementation of `apply_condition(entity_id, entity_condition_immunities, entity_current_conditions, entity_concentrating, condition_to_apply, source_spell_or_effect)`.

## Acceptance Criteria
- [ ] File exists at `.claude/skills/atomic-ops/operations/condition_application.py`
- [ ] Immunity check rejects immune conditions
- [ ] Concentration break ends current concentration
- [ ] Three stacking modes work (no_stack, stack, replace)
- [ ] Returns dict matching output schema
