# Merchant Loop

## Status
NEW

## Location
`.claude/skills/merchant/SKILL.md` + `.claude/skills/merchant/contracts/`

## What
Merchant encounter loop for buying, selling, and bartering. Handles inventory browsing, price negotiation (Persuasion checks for discounts), and gold tracking. Dispatched by scene loop when `encounter_type == "merchant"`.

## Resolution Flow
1. Receive merchant encounter (merchant_id, inventory, price_modifier, disposition)
2. Present merchant inventory with prices
3. Offer actions via action-prompt: buy, sell, barter, browse, leave
4. For buy: deduct gold, add item to party inventory
5. For sell: add gold, remove item from party inventory (sell at 50% base price)
6. For barter: Persuasion check vs DC to get discount (5-20% off)
7. Return outcome with transaction log

## Contracts Needed
- `merchant-action-contract.json` — input: action (buy/sell/barter), item_id, quantity, roll (for barter)
- `merchant-outcome-contract.json` — output: transaction_log, gold_change, items_added, items_removed

## Dependencies
- action-prompt skill (user choices)
- campaign state (party_gold, inventory)
- entity system (merchant NPC data)
