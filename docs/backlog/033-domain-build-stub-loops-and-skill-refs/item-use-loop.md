# Item-Use Loop

## Status
NEW

## Location
`.claude/skills/item-use/SKILL.md` + `.claude/skills/item-use/contracts/`

## What
Item-use loop for consuming potions, reading scrolls, activating magic items, and using mundane equipment outside of combat. In combat, item use is handled by the combat loop's action economy. This loop handles non-combat item interactions. Dispatched by scene loop when `encounter_type == "item-use"`.

## Resolution Flow
1. Receive item-use action (character_id, item_id, target)
2. Validate item exists in character/party inventory
3. Determine item type and effect:
   - Potion: apply healing/buff, consume item
   - Scroll: check if caster can use (class spell list + level), apply effect, consume
   - Magic item: check attunement slots (max 3), apply effect
   - Mundane: apply situational effect (rope, torch, tools)
4. If item requires a check (scroll casting above spell level): prompt for Arcana check
5. Update inventory (remove consumed items, track charges)
6. Return outcome with effect applied

## Contracts Needed
- `item-use-action-contract.json` — input: character_id, item_id, target, context
- `item-use-outcome-contract.json` — output: effect_applied, item_consumed, charges_remaining, check_result

## Dependencies
- action-prompt skill (user choices)
- campaign state (inventory, attunement slots)
- character templates (spell lists for scroll validation)
- atomic-ops (healing, buff application)
