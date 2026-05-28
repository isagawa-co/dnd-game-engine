# Build Rest Operations

## Context
Create rest_operations.py implementing long rest, short rest, and hit dice recovery.

## Type
BUILD

## Execution
inline

## Dependencies
- 001

## Requirements
- Create `.claude/skills/rest/rest_operations.py`
- `long_rest(party_state)` — restore all HP, spell slots, hit dice; return recovery dict
- `short_rest(party_state)` — restore half HP (rounded up), allow 1 hit die roll; return recovery dict
- `roll_hit_die(die_type, con_modifier)` — roll hit die + CON mod, return dict with roll details
- `restore_spell_slots(pc_state)` — restore all spell slots per class table
- `restore_hit_dice(pc_state)` — restore up to level amount of hit dice
- HP capped at max (no overheal)
- Uses random for dice rolls (seeded for testing)

## Acceptance Criteria
- [ ] `.claude/skills/rest/rest_operations.py` exists
- [ ] `long_rest` function exists and returns recovery dict
- [ ] `short_rest` function exists and returns recovery dict
- [ ] `roll_hit_die` function exists and returns roll details
- [ ] HP never exceeds max_hp

## Gates Satisfied
- BUILD-03, FUNC-01, FUNC-02, FUNC-03

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
