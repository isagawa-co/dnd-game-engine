# Build Challenge Outcome Contract

## Context
Create the JSON schema contract for challenge outcome outputs — defines the result structure returned after challenge resolution.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `.claude/skills/challenge/contracts/challenge-outcome-contract.json`
- Schema fields from backlog design doc: challenge_type, success, result_code, margin, challenge_name, consequence, state_mutations
- result_code enum: success, partial_success, failure, critical_failure
- consequence.type enum: none, damage, exhaustion, time_loss, enemy_alert
- JSON Schema draft-07

## Acceptance Criteria
- [ ] `.claude/skills/challenge/contracts/challenge-outcome-contract.json` exists
- [ ] File is valid JSON with `$schema` field
- [ ] Contains all required fields from design doc
- [ ] result_code covers all 4 outcome types

## Gates Satisfied
- BUILD-02

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
