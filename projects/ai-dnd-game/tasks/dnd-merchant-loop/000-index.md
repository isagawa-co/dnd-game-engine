# D&D Merchant Loop — Task Index

## Goal
Build the merchant loop sub-skill: shop inventory display, buy/sell transactions, price negotiation, and outcome contracts.

## Source
→ [[docs/backlog/013-dnd-build-merchant-loop.md]]
→ [[docs/backlog/013-dnd-build-merchant-loop/transaction-contract.md]]

## Tasks

| # | Task | Type | Dependencies | Status |
|---|------|------|-------------|--------|
| 001 | [[001-build-transaction-contract]] | BUILD | none | pending |
| 002 | [[002-build-shop-inventory-contract]] | BUILD | none | pending |
| 003 | [[003-build-negotiation-contract]] | BUILD | none | pending |
| 004 | [[004-build-merchant-skill-md]] | BUILD | 001-003 | pending |
| 005 | [[005-test-validate-all-merchant]] | TEST | 001-004 | pending |

## Gate Contract
→ [[gate-contract.md]]

## Deliverables
- `projects/ai-dnd-game/.claude/skills/merchant/contracts/merchant-loop-contract.json` — transaction contract
- `projects/ai-dnd-game/.claude/skills/merchant/contracts/shop-inventory-contract.json` — shop inventory contract
- `projects/ai-dnd-game/.claude/skills/merchant/contracts/negotiation-contract.json` — negotiation contract
- `projects/ai-dnd-game/.claude/skills/merchant/SKILL.md` — merchant skill definition
