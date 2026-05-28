# Build Item Effect Catalog

## Context
Create the item-effect-catalog.json — defines all item effects (potions, equipment, magical items) with their properties.

## Type
BUILD

## Execution
inline

## Dependencies
- None

## Requirements
- Create `.claude/skills/item-use/contracts/item-effect-catalog.json`
- Include items from backlog contract: potion_healing (1d4+4 HP), potion_resistance_fire (grant fire resistance, 1 hour), leather_armor (AC 11)
- Each item entry: id, name, effect, amount/value, duration, consumed flag
- Cover all item types: potion, equipment (armor/weapon), magical_item, consumable (scroll, wand)
- At least 8 catalog entries covering variety of types

## Acceptance Criteria
- [ ] `.claude/skills/item-use/contracts/item-effect-catalog.json` exists
- [ ] File is valid JSON
- [ ] Contains at least 8 item entries
- [ ] Covers potions, equipment, magical items, and consumables

## Gates Satisfied
- BUILD-02, FUNC-02

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
