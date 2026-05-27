# Build Rest Loop Contract

## Context
Create the JSON contract defining rest loop input/output structures.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `.claude/skills/rest/rest-loop-contract.json`
- Define input schema: rest_type, party_location, location_safety, duration_hours, party_pcs, conditions_before
- Define long rest output: result_code, party_recovery (hp, spell_slots, hit_dice, conditions)
- Define short rest output: result_code, party_recovery (hp, hit_die_rolled)
- Define outcome codes: long_rest_completed, short_rest_completed, interrupted_rest, rest_refused

## Acceptance Criteria
- [ ] `.claude/skills/rest/rest-loop-contract.json` exists
- [ ] File is valid JSON
- [ ] Contains input_schema, long_rest_output, short_rest_output sections

## Gates Satisfied
- BUILD-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
