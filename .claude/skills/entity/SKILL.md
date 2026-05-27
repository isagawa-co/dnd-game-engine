# Entity System — Skill Definition

**Type:** Prescriptive
**Domain:** D&D 5e Entity Management

## What

4-tier entity system for D&D 5e: Stat Block, Named Monster, NPC, PC. Each tier adds complexity. Validation enforces D&D 5e rules.

## Contracts

| Contract | Purpose |
|----------|---------|
| `contracts/entity-tiers-contract.json` | 4-tier architecture definition |
| `contracts/entity-validation-contract.json` | 8 validation rules (ENT-VAL-001 to 008) |
| `contracts/personality-schema.json` | Personality layer for Tier 2+ |

## Tiers

| Tier | Type | Use Case | Fields Added |
|------|------|----------|--------------|
| 1 | Stat Block | Generic monsters, guards | AC, HP, abilities, actions |
| 2 | Named Monster | Boss monsters, unique creatures | + personality (voice, motivation, morale) |
| 3 | NPC | Quest-givers, merchants, allies | + social (relationships, goals, fears) |
| 4 | PC | Player characters | + class, level, spells, inventory, proficiencies |

## Validation Flow

1. Load entity JSON
2. Determine tier from `entity_type` field
3. Validate tier-specific required fields
4. Run ENT-VAL rules (ability scores, HP, AC, etc.)
5. For Tier 4: validate proficiency, spell slots, inventory weight, hit dice
6. Return pass/fail with error list

## Implementation

- `projects/ai-dnd-game/src/entity/entity_loader.py` — validation logic
- `projects/ai-dnd-game/src/entity/__init__.py` — package exports

## Fixtures

Test fixtures in `fixtures/`:
- `goblin-stat-block.json` (Tier 1)
- `dire-wolf-stat-block.json` (Tier 1)
- `king-grol-named-monster.json` (Tier 2)
- `gundren-rockseeker-npc.json` (Tier 3)
- `sildar-hallwinter-pc.json` (Tier 4)
