# Build Transaction Contract

## Context
Create the merchant transaction contract JSON schema — defines buy/sell request and outcome structures.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `projects/ai-dnd-game/.claude/skills/merchant/contracts/merchant-loop-contract.json`
- Schema defines transaction_request and transaction_outcome structures per backlog 013 transaction-contract.md
- Required fields for request: transaction_type (buy|sell), merchant_id, actor_pc, items array
- Required fields for outcome: transaction_type, success, result_code, gold_change, party_gold_after, state_mutations
- Result codes: transaction_success, insufficient_gold, insufficient_inventory, negotiation_success
- Validation: quantity >= 1, unit_price > 0, party_gold_after >= 0
- JSON Schema draft-07

## Acceptance Criteria
- [ ] `projects/ai-dnd-game/.claude/skills/merchant/contracts/merchant-loop-contract.json` exists
- [ ] File is valid JSON with `$schema` field
- [ ] Contains transaction_request and transaction_outcome definitions

## Gates Satisfied
- BUILD-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
