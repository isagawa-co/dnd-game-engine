# Build Combat Action Contract

## Context
Create the combat action contract JSON schema — defines action resolution structures for attack, cast spell, ability check, dodge, disengage, dash, and bonus actions.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `projects/ai-dnd-game/.claude/skills/combat/contracts/combat-action-contract.json`
- Schema defines action_request: actor_id, action_type (attack|cast_spell|ability_check|dodge|disengage|dash|help|ready), target_id, parameters
- Schema defines action_result: actor_id, action_type, success, result_code, damage_dealt, conditions_applied, state_mutations
- Attack action: dispatches to attack-roll-contract (atomic_ops/attack_operations)
- Cast spell: spell_dc, range_check, component_requirements, concentration
- Ability check: dispatches to ability-check-contract (atomic_ops/check_operations)
- Dodge: grants disadvantage on attacks against until next turn
- Disengage: no opportunity attacks
- Dash: doubles movement
- Result codes: action_hit, action_miss, action_critical, spell_success, spell_resisted, action_dodged
- JSON Schema draft-07

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/.claude/skills/combat/contracts/combat-action-contract.json` exists
- [ ] File is valid JSON with `$schema` field
- [ ] Contains action_request and action_result definitions
- [ ] All action types present (attack, cast_spell, ability_check, dodge, disengage, dash, help, ready)
- [ ] All result codes present

## Gates Satisfied
- BUILD-03

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
