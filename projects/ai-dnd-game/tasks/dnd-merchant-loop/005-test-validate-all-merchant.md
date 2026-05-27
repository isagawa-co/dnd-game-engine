# Test Validate All Merchant Contracts

## Context
Validate all merchant skill deliverables: JSON schemas are valid, SKILL.md exists and references all contracts.

## Type
TEST

## Execution
inline

## Dependencies
- 001-build-transaction-contract
- 002-build-shop-inventory-contract
- 003-build-negotiation-contract
- 004-build-merchant-skill-md

## Requirements
- Validate all 3 JSON contract files are valid JSON with $schema field
- Validate SKILL.md exists and contains references to all 3 contracts
- Validate merchant-loop-contract.json has transaction_request and transaction_outcome definitions
- Validate shop-inventory-contract.json has merchant inventory definitions
- Validate negotiation-contract.json has price calculation fields
- Run validation via python3 json.loads() and file existence checks

## Acceptance Criteria
- [ ] All 3 JSON files parse as valid JSON
- [ ] All 3 JSON files have `$schema` field
- [ ] SKILL.md references all 3 contracts
- [ ] All files exist at correct paths under `projects/ai-dnd-game/.claude/skills/merchant/`

## Gates Satisfied
- TEST-01

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
