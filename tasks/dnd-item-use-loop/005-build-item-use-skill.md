# Build Item-Use Skill Definition

## Context
Create the SKILL.md — skill definition for item-use loop, following wiki-link tiered indexing pattern.

## Type
BUILD

## Execution
inline

## Dependencies
- 001-build-item-use-contract
- 002-build-item-effect-catalog
- 003-build-attunement-rules
- 004-build-validation-rules

## Requirements
- Create `.claude/skills/item-use/SKILL.md`
- Identity section: skill name, purpose, scope
- Contracts section with wikilinks to all 4 JSON contracts
- Item types section referencing catalog
- Validation flow: check inventory → check requirements → check action cost → apply effect → consume if needed
- Outcome codes: item_used_success, item_not_found, attunement_required, action_blocked, target_invalid
- Integration: references scene-loop (007), atomic-ops effect-operations-contract (003)

## Acceptance Criteria
- [ ] `.claude/skills/item-use/SKILL.md` exists
- [ ] Contains identity, contracts, item types, validation flow, outcomes sections
- [ ] Uses wikilinks to reference contracts (no inline duplication)
- [ ] References scene-loop and atomic-ops integration points

## Gates Satisfied
- BUILD-05, FUNC-05

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
