# Character Pool Contract

## Status
NEW

## Location
`contracts/character-pool-contract.json`

## Purpose
Defines the schema for shared character storage and campaign-character references. Characters live in `characters/` and campaigns reference them by ID.

## Character File Schema

Each character stored at: `characters/<character-id>.json`

```json
{
  "id": "honu-tortle-fighter",
  "entity_type": "pc",
  "name": "Honu",
  "character_class": "fighter",
  "race": "tortle",
  "level": 1,
  "xp": 0,
  "ability_scores": { "strength": 17, "dexterity": 13, "constitution": 14, "intelligence": 8, "wisdom": 13, "charisma": 10 },
  "hp": 12,
  "max_hp": 12,
  "ac": 19,
  "hit_dice_detail": { "die_type": "d10", "number": 1, "remaining": 1 },
  "proficiency_bonus": 2,
  "proficiencies": {},
  "class_features": [],
  "racial_features": [],
  "inventory": [],
  "gold": 0,
  "personality": {},
  "creation_metadata": {
    "creation_method": "standard_array",
    "created_date": "2026-05-27",
    "source_campaign": "campaign-2026-05-27-002"
  },
  "campaign_history": [
    {
      "campaign_id": "campaign-2026-05-27-002",
      "joined_at_level": 1,
      "current_level": 1,
      "status": "active"
    }
  ]
}
```

## Campaign Reference Schema

Campaign `party.json` references character IDs instead of embedding full entities:

```json
{
  "campaign_id": "campaign-2026-05-27-002",
  "party_size": 4,
  "characters": [
    {
      "character_id": "honu-tortle-fighter",
      "party_position": 1,
      "snapshot_level": 1,
      "joined_date": "2026-05-27"
    }
  ]
}
```

## Resolution Rules
- Campaign loader reads `party.json`, resolves each `character_id` from `characters/<id>.json`
- If character file not found: error, party incomplete
- Character `level` in pool is the character's current canonical level
- Campaign `snapshot_level` records what level the character was when they joined

## Validation Rules
- Character files must pass CHAR-001 through CHAR-008 from character-creation-contract.json
- Character ID must be unique across pool (no duplicates)
- Character ID format: `<name-kebab>-<race>-<class>` (e.g., `honu-tortle-fighter`)

## Dependencies
- Must conform to character-creation-contract.json output_schema (Tier 4 entity)
- Used by character-creation-loop (Part 5: save)
- Used by campaign loader (game-play command)
