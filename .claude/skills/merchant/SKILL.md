# Merchant Loop — Skill Definition

## Identity

| Key | Value |
|-----|-------|
| Skill | merchant |
| Type | sub-loop |
| Parent | scene-loop |
| Purpose | Handle buying, selling, and bartering with NPCs including inventory browsing and price negotiation |

## Vocabulary

| Term | Definition |
|------|-----------|
| Base Price | Standard PHB price for an item |
| Sell Price | 50% of base price (standard D&D 5e rule) |
| Price Modifier | Multiplier based on merchant disposition and local economy (0.8-1.5x) |
| Barter | Persuasion check to negotiate a discount (5-20% off purchase price) |

## Contracts

| Contract | File |
|----------|------|
| Input | -> [[contracts/merchant-action-contract.json]] |
| Output | -> [[contracts/merchant-outcome-contract.json]] |

## Resolution Flow

1. Scene loop sends merchant encounter (merchant_id, inventory, price_modifier, disposition)
2. Present merchant and their available inventory with prices
3. Offer actions via action-prompt: buy, sell, barter, browse, leave
4. Resolve action:
   - **Buy:** Validate party has enough gold. Deduct gold, add item to party inventory.
   - **Sell:** Add gold (50% base price), remove item from party inventory.
   - **Barter:** Persuasion check vs DC 15. Success = 10% discount. Beat by 5+ = 20% discount. Fail = no discount, merchant offended (-1 disposition).
   - **Browse:** Show full inventory with descriptions and prices. No state change.
   - **Leave:** End merchant encounter. Return to scene.
5. Loop until user chooses "leave" or runs out of gold
6. Return outcome with transaction log

## Agent Execution

1. **Identify the merchant** from the act file — name, shop type, specialty
2. **Present inventory** — list items with prices (base price * price_modifier)
3. **Use action-prompt** with `merchant` context for buy/sell/barter options
4. **For purchases:** Confirm item and quantity, check gold, execute transaction
5. **For sales:** Show party inventory, let user pick items to sell at 50% value
6. **For barter:** Prompt "Make a Persuasion check (DC 15)" — apply discount on success
7. **Update state** — modify party_gold, inventory in campaign_state.json

## Integration

- **Depends on:** action-prompt (user choices), campaign state (party_gold, inventory), entity system (merchant NPC)
- **Returns to:** scene-loop (outcome dict with transaction_log, gold_change, items_added, items_removed)
- **State updates:** campaign_state.json → party_gold, inventory
