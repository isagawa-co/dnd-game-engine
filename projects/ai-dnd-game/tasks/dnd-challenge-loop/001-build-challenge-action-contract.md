# Build Challenge Action Contract

## Context
Create the JSON schema contract for challenge action inputs — defines what data flows into the challenge resolution system.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `.claude/skills/challenge/contracts/challenge-action-contract.json`
- Schema fields from backlog design doc: challenge_type, challenge_name, actor_pc, skill_used, difficulty_class, attempt_number, bonus_modifiers, roll_result
- challenge_type enum: climb, swim, jump, balance, push_pull, hide, sneak, pick_lock, break_door, disable_trap, investigate, arcana, history, religion, nature, perception, insight
- skill_used enum: athletics, acrobatics, sleight_of_hand, investigation, arcana, history, religion, nature, perception, insight, stealth
- JSON Schema draft-07

## Acceptance Criteria
- [ ] `.claude/skills/challenge/contracts/challenge-action-contract.json` exists
- [ ] File is valid JSON with `$schema` field
- [ ] Contains all required fields from design doc
- [ ] challenge_type enum covers all 5 categories (physical, stealth, locks, knowledge, perception)

## Gates Satisfied
- BUILD-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
