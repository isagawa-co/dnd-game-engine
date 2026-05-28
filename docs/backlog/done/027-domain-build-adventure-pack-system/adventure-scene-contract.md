# Adventure Scene Contract — Act Schema

## Status
NEW

## Location
`workspace:contracts/adventure-scene-contract.json`

## What It Does
Defines the JSON schema for act files. Every act file follows this contract. The game loop validates against it before presenting scenes to the player.

## Schema Fields

### Required
- `act_id` — unique identifier (e.g., `ch1-act-II`)
- `chapter` — chapter number (integer)
- `act` — act numeral (string: "I", "II", "III", etc.)
- `title` — human-readable title
- `level_range` — [min, max] party level for this act
- `location` — object with `name`, `description`, `environment`
- `read_aloud` — boxed text the DM reads to set the scene (string or array of strings for multi-part)
- `encounters` — array of encounter objects
- `transitions` — object mapping outcomes to next act_id

### Optional
- `npcs` — array of NPC objects present in this act (id, name, attitude, dialog_hooks)
- `loot` — array of loot objects (item_id from manifest, quantity, location)
- `skill_checks` — array of checks (skill, dc, success text, failure text)
- `traps` — array of trap objects (trigger, dc, damage, description)
- `secrets` — array of discoverable information (perception/investigation DC, info revealed)
- `conditions` — prerequisites for this act to trigger (e.g., "has_item: gundren_map")
- `dm_notes` — agent-only guidance for running this act

### Encounter Object
```json
{
  "type": "combat | social | challenge | trap",
  "trigger": "automatic | conditional | player_action",
  "surprise": false,
  "enemies": [
    {"monster_id": "goblin", "count": 4, "position": "description"}
  ],
  "tactics": "How enemies behave",
  "difficulty": "easy | medium | hard | deadly",
  "reward_xp": 200
}
```

### Transition Object
```json
{
  "combat_won": "ch1-act-III",
  "combat_lost": "ch1-act-II-capture",
  "fled": "ch1-act-I",
  "social_success": "ch2-act-I",
  "default": "ch1-act-III"
}
```

## Dependencies
- folder-restructure (needs adventures/ path to exist)
