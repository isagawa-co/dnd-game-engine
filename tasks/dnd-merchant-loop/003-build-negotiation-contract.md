# Build Negotiation Contract

## Context
Create the price negotiation contract JSON schema — defines persuasion-based price reduction mechanics.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `.claude/skills/merchant/contracts/negotiation-contract.json`
- Schema defines negotiation request and outcome per backlog 013 transaction-contract.md
- Price calculation: base_price x (1 - relationship_discount - negotiation_discount)
- Relationship discount: 0.10 if relationship >= 10, 0.05 if relationship >= 0, else 0
- Negotiation discount: 0.20 if persuasion_check >= DC, else 0
- Persuade DC: 12 (default)
- Required fields: actor_pc, merchant_id, skill_used (persuasion|intimidation), dc, roll_result, discount_applied, final_price_modifier
- JSON Schema draft-07

## Acceptance Criteria
- [ ] `.claude/skills/merchant/contracts/negotiation-contract.json` exists
- [ ] File is valid JSON with `$schema` field
- [ ] Contains price calculation formula fields

## Gates Satisfied
- BUILD-03

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
