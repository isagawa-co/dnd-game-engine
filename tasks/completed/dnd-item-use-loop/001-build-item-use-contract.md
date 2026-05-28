# Build Item-Use Loop Contract

## Context
Create the item-use-loop-contract.json — the input/output contract for all item usage actions during encounters.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `.claude/skills/item-use/contracts/item-use-loop-contract.json`
- Input schema from backlog 016 item-effect-contract: action_type, actor_pc, target_pc, item_id, item_type, action_cost, requires_attunement, requires_check, check_dc
- Output schema: action_type, success, result_code, item_id, item_name, user_pc, target_pc, effect_applied, effect_amount, effect_type, effect_duration, item_consumed, item_count_before, item_count_after, pc_hp_before, pc_hp_after, state_mutations, narrative
- Result codes: item_used_success, item_not_found, attunement_required, action_blocked, target_invalid
- JSON Schema draft-07

## Acceptance Criteria
- [ ] `.claude/skills/item-use/contracts/item-use-loop-contract.json` exists
- [ ] File is valid JSON with `$schema` field
- [ ] Input schema has all required fields from contract
- [ ] Output schema has all result codes and state_mutations

## Gates Satisfied
- BUILD-01, FUNC-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
