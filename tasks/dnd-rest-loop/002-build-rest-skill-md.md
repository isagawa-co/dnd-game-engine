# Build Rest SKILL.md

## Context
Create the SKILL.md for the rest sub-skill defining identity, operations, and contracts.

## Type
BUILD

## Execution
inline

## Dependencies
- 001

## Requirements
- Create `.claude/skills/rest/SKILL.md`
- Define skill identity: rest loop manager
- List operations: long_rest, short_rest, roll_hit_die, check_interruption
- Reference rest-loop-contract.json
- Define condition removal rules
- Define location safety modifiers

## Acceptance Criteria
- [ ] `.claude/skills/rest/SKILL.md` exists
- [ ] Contains identity, operations table, contracts reference

## Gates Satisfied
- BUILD-02

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
