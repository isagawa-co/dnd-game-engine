# Build Shop Inventory Contract

## Context
Create the shop inventory contract JSON schema — defines merchant inventory display structure.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `.claude/skills/merchant/contracts/shop-inventory-contract.json`
- Schema defines merchant inventory structure per backlog 013 transaction-contract.md
- Required fields: merchant_id, merchant_name, location, relationship_value, inventory array, accepts_trades, price_discount
- Inventory item fields: item_id, name, quantity, base_price, current_price, description
- JSON Schema draft-07

## Acceptance Criteria
- [ ] `.claude/skills/merchant/contracts/shop-inventory-contract.json` exists
- [ ] File is valid JSON with `$schema` field
- [ ] Contains merchant inventory item definitions

## Gates Satisfied
- BUILD-02

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
