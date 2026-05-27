# Item-Use Loop — Skill Definition

## Identity

| Key | Value |
|-----|-------|
| Skill | item-use |
| Type | sub-loop |
| Parent | scene-loop |
| Purpose | Handle using potions, scrolls, magic items, and mundane equipment outside of combat |

## Vocabulary

| Term | Definition |
|------|-----------|
| Consumable | Item destroyed on use: potions, scrolls, single-use items |
| Charges | Remaining uses on a magic item before it needs recharging (dawn reset or permanent depletion) |
| Attunement | Bond required for certain magic items; max 3 attuned items per character |
| Scroll Casting | Using a spell scroll; requires the spell on your class list. If spell level > your max, Arcana check DC 10 + spell level |

## Contracts

| Contract | File |
|----------|------|
| Input | -> [[contracts/item-use-action-contract.json]] |
| Output | -> [[contracts/item-use-outcome-contract.json]] |

## Resolution Flow

1. Scene loop sends item-use action (character_id, item_id, target)
2. Validate item exists in character or party inventory
3. Determine item type and resolve:
   - **Potion:** Apply effect (healing, buff, resistance). Consume item. No check needed.
   - **Scroll:** Check if caster has spell on class list. If spell level > max slot level, prompt Arcana check DC 10 + spell level. On success: apply effect, consume scroll. On failure: scroll is destroyed with no effect.
   - **Magic Item (charges):** Check charges remaining. Apply effect. Decrement charges. If charges = 0, check if item is destroyed or recharges at dawn.
   - **Magic Item (attunement):** Check attunement slots (max 3). If not attuned, requires short rest to attune. Once attuned, apply effect.
   - **Mundane:** Apply situational effect (rope = climb advantage, torch = light, tools = proficiency on checks).
4. Update inventory (remove consumed items, update charges)
5. Return outcome with effect applied

## Agent Execution

1. **Identify the item** from party inventory or character equipment
2. **Validate usage** — does the character have the item? Can they use it?
3. **Present options** using action-prompt with `item_use` context
4. **For potions:** "You drink the Potion of Healing. Roll 2d4 + 2 for healing."
5. **For scrolls:** Check class spell list. If over-level: "Make an Arcana check (DC [10 + spell level])"
6. **For magic items:** Describe activation, apply effect
7. **Update state** — remove consumed items, update charges in campaign_state.json

## Integration

- **Depends on:** action-prompt (user choices), campaign state (inventory, attunement), character templates (spell lists for scroll validation), atomic-ops (healing, buffs)
- **Returns to:** scene-loop (outcome dict with effect_applied, item_consumed, charges_remaining)
- **State updates:** campaign_state.json → inventory, item charges
