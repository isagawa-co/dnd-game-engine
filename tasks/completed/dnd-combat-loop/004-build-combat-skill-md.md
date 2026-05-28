# Build Combat SKILL.md

## Context
Create the combat skill definition file — describes the combat loop sub-skill architecture, contracts, and flow.

## Type
BUILD

## Execution
inline

## Dependencies
- 001-build-combat-loop-contract
- 002-build-combat-state-contract
- 003-build-combat-action-contract

## Requirements
- Create `.claude/skills/combat/SKILL.md`
- Follow existing SKILL.md pattern (see .claude/skills/rest/SKILL.md for reference)
- Sections: Identity, Philosophy, Contracts table, Core Operations, Combat Flow, Outcome Resolution, Testing Requirements, Communication Guidelines
- Reference all 3 contracts via wiki-links
- Describe combat flow: initialize (roll initiative) -> execute rounds (turn order) -> resolve actions -> apply damage/effects -> check outcomes -> return result
- Document integration with scene-loop (007) and atomic-ops (003): attack_operations, damage_operations, effect_operations, check_operations
- Document death save mechanics: 3 successes = stabilize, 3 failures = death

## Acceptance Criteria
- [ ] `.claude/skills/combat/SKILL.md` exists
- [ ] References all 3 contracts
- [ ] Describes combat loop flow
- [ ] Follows existing SKILL.md pattern
- [ ] Documents death save mechanics

## Gates Satisfied
- BUILD-04

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
