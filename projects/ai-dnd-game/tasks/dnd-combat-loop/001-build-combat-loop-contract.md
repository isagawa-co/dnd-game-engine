# Build Combat Loop Contract

## Context
Create the main combat loop contract JSON schema — defines combat initialization input, round execution, and combat outcome structures.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `projects/ai-dnd-game/.claude/skills/combat/contracts/combat-loop-contract.json`
- Schema defines combat_input and combat_outcome structures per backlog 010
- Required input fields: encounter_id, party_pcs (array with id, hp, max_hp, ac, dex_modifier, attack_bonus, damage_dice, damage_type), enemies (same structure), terrain
- Required outcome fields: encounter_id, result_code, rounds_elapsed, surviving_pcs, surviving_enemies, xp_earned, loot
- Result codes: victory, defeat, draw, escape
- Initiative: 1d20 + dex_modifier per combatant
- Turn order: highest initiative first
- JSON Schema draft-07

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/.claude/skills/combat/contracts/combat-loop-contract.json` exists
- [ ] File is valid JSON with `$schema` field
- [ ] Contains combat_input and combat_outcome definitions
- [ ] All result codes present (victory, defeat, draw, escape)

## Gates Satisfied
- BUILD-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
