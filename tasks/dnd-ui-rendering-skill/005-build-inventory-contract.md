# Task 005: Build Inventory Contract

## Action
Create `contracts/inventory-contract.json` — JSON schema for inventory display input/output.

## Deliverable
`.claude/skills/ui-rendering/contracts/inventory-contract.json`

## Acceptance Criteria
- [ ] File exists at correct path
- [ ] Valid JSON schema with input_schema and output_schema
- [ ] Input covers: items (name, quantity, weight, value), total_weight, carrying_capacity, party_gold
- [ ] Output specifies terminal_text format with item list, weight summary, gold display
- [ ] Includes validation rules and example

## Dependencies
001

## Gate
CONTRACT-004: `file_exists: .claude/skills/ui-rendering/contracts/inventory-contract.json`
