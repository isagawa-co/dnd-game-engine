# Build Combat State Contract

## Context
Create the combat state contract JSON schema — defines per-round state tracking, combatant status, action economy, and condition tracking.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `projects/ai-dnd-game/.claude/skills/combat/contracts/combat-state-contract.json`
- Schema defines combatant_state: id, name, side (party|enemy), hp, max_hp, ac, initiative_roll, conditions, concentrating, death_saves
- Schema defines round_state: round_number, turn_order (array of combatant IDs), current_turn_index, phase (initiative|combat|resolved)
- Action economy per turn: action (bool), bonus_action (bool), reaction (bool), movement (int remaining)
- Death saves: successes (0-3), failures (0-3), stable (bool)
- Condition tracking: condition_id, duration_remaining, source
- JSON Schema draft-07

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/.claude/skills/combat/contracts/combat-state-contract.json` exists
- [ ] File is valid JSON with `$schema` field
- [ ] Contains combatant_state and round_state definitions
- [ ] Action economy fields present
- [ ] Death saves fields present

## Gates Satisfied
- BUILD-02

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
