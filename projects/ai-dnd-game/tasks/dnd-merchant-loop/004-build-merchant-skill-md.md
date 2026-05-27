# Build Merchant SKILL.md

## Context
Create the merchant skill definition file — describes the merchant loop sub-skill architecture, contracts, and flow.

## Type
BUILD

## Execution
inline

## Dependencies
- 001-build-transaction-contract
- 002-build-shop-inventory-contract
- 003-build-negotiation-contract

## Requirements
- Create `projects/ai-dnd-game/.claude/skills/merchant/SKILL.md`
- Follow existing SKILL.md pattern (see content/SKILL.md for reference)
- Sections: What, Architecture, Contracts table, Flow, Error Handling
- Reference all 3 contracts via wiki-links
- Describe merchant loop flow: display inventory → player action → validate → execute → return outcome
- Document integration with scene-loop (007) and ability-check-contract (003)

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/.claude/skills/merchant/SKILL.md` exists
- [ ] References all 3 contracts
- [ ] Describes merchant loop flow
- [ ] Follows existing SKILL.md pattern

## Gates Satisfied
- BUILD-04

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
