# Build Item Files — Armor, Gear, and Magic Items

## Context
Create Tier 3 item files for armor, adventuring gear, potions/scrolls, and magical items. Each file must conform to item-schema.json.

## Type
BUILD

## Execution
inline

## Dependencies
- 003, 009

## Phase Gate
- [ ] `.claude/skills/content/contracts/item-schema.json` exists
- [ ] `content/lost-mine-phandelver/manifest.json` exists

## Requirements
- **Armor (3):**
  - Create `leather-armor.json` — armor, common, 10 lb, AC 11 + Dex
  - Create `chain-mail.json` — armor, common, 55 lb, AC 16, Str 13 required, stealth disadvantage
  - Create `shield.json` — shield, common, 6 lb, AC +2
- **Potions/Scrolls (2):**
  - Create `potion-of-healing.json` — potion, common, 0.5 lb, heals 2d4+2
  - Create `spell-scroll.json` — scroll, common, 0 lb, 1st level spell
- **Adventuring Gear (3):**
  - Create `rations.json` — wondrous_item, common, 2 lb
  - Create `rope.json` — wondrous_item, common, 10 lb, 50 feet hempen
  - Create `lamp.json` — wondrous_item, common, 1 lb
- **Magical Items (3):**
  - Create `weapon-of-warning.json` — weapon, uncommon, attunement required, advantage on initiative
  - Create `wand-of-magic-missiles.json` — wand, uncommon, 7 charges, recharge at dawn
  - Create `ring-of-protection.json` — wondrous_item, rare, attunement required, +1 AC and saves
- All files in `content/lost-mine-phandelver/items/`
- All files must conform to item-schema.json

## Acceptance Criteria
- [ ] All 11 item files exist (3 armor + 2 potions/scrolls + 3 gear + 3 magical)
- [ ] Total item files in `items/` directory equals 18 (7 weapons + 11 this task)
- [ ] Magical items have correct rarity and attunement settings
- [ ] All files are valid JSON with required fields

## Gates Satisfied
- BUILD-12, FUNC-06

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
