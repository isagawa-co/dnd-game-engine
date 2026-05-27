# Character Creation Workflow Reference

Reference document for the character-creation-loop execution model. Defines the 4-step party creation flow, ability score generation, HP calculation, and skill/equipment assignment.

## Contracts

| Contract | Path | Purpose |
|----------|------|---------|
| Action | `contracts/character-creation-action-contract.json` | Input schema for character creation requests |
| Outcome | `contracts/character-creation-outcome-contract.json` | Output schema for creation results with complete PC objects |
| Party Validation | `contracts/character-creation-party-validation-contract.json` | Validation rules for party composition and PC integrity |

## 4-Step Party Creation Flow

### Overview

```
Input (action contract) → validate_action() → create_character() x N → build_party() → validate_outcome() → Output (outcome contract)
```

1. **validate_action()** — Verify the incoming action conforms to the action contract
2. **create_character()** — For each character entry, build a complete PC object
3. **build_party()** — Collect all PCs into the party array
4. **validate_outcome()** — Run the party through the party-validation contract

### Step 1: validate_action()

Verify the incoming action conforms to `character-creation-action-contract.json`.

- `party_size` must be 1-6 (integer)
- `mode` must be one of: `wizard`, `random`, `preset`
- `characters` array must have 1-6 entries matching `party_size`
- Each character entry requires: `name` (non-empty string), `race` (valid race), `class` (valid class)
- Optional: `ability_scores` (array of 6 integers 3-18, or null to roll during creation)

Reject with error if any field is missing or out of range.

### Step 2: create_character()

For each character entry in the action, build a complete PC object:

#### 2a. Validate Race

Check that `race` is in the extended race registry:
- Valid races: human, elf, dwarf, halfling, gnome, half-elf, half-orc, tiefling, dragonborn
- Reject if race is not in the registry

#### 2b. Validate Class

Check that `class` is in the extended class registry:
- Valid classes: barbarian, bard, cleric, druid, fighter, monk, paladin, ranger, rogue, sorcerer, warlock, wizard
- Reject if class is not in the registry

#### 2c. Calculate Ability Scores

If `ability_scores` is provided (array of 6 integers), use them directly as [STR, DEX, CON, INT, WIS, CHA].

If `ability_scores` is null, generate using the creation method from player settings:
- **4d6_drop_lowest**: Roll 4d6, drop the lowest die, sum remaining 3. Repeat for each ability. Range: 3-18.
- **standard_array**: Assign from [15, 14, 13, 12, 10, 8] in order.
- **point_buy**: Allocate from a point budget (27 points, scores start at 8, cost varies).
- **2d6_plus_6**: Roll 2d6+6 for each ability. Range: 8-18.

Apply racial modifiers after base generation. Final scores capped at 20.

Output: `{ "STR": int, "DEX": int, "CON": int, "INT": int, "WIS": int, "CHA": int }`

#### 2d. Calculate HP

Level 1 HP formula: `class_hit_die_max + CON_modifier`

CON modifier = `floor((CON - 10) / 2)`

Hit die by class:

| Class | Hit Die |
|-------|---------|
| barbarian | d12 |
| fighter, paladin, ranger | d10 |
| bard, cleric, druid, monk, rogue, warlock | d8 |
| sorcerer, wizard | d6 |

Example: Fighter with CON 16 → CON modifier = +3 → HP = 10 + 3 = 13

Set both `hp_current` and `hp_max` to the calculated value.

#### 2e. Generate Skill Proficiencies

Select skill proficiencies per class. Each class specifies how many skills to choose and from which list:

| Class | Choose | From |
|-------|--------|------|
| barbarian | 2 | animal handling, athletics, intimidation, nature, perception, survival |
| bard | 3 | any skill |
| cleric | 2 | history, insight, medicine, persuasion, religion |
| druid | 2 | arcana, animal handling, insight, medicine, nature, perception, religion, survival |
| fighter | 2 | acrobatics, animal handling, athletics, history, insight, intimidation, perception, survival |
| monk | 2 | acrobatics, athletics, history, insight, religion, stealth |
| paladin | 2 | athletics, insight, intimidation, medicine, persuasion, religion |
| ranger | 3 | animal handling, athletics, insight, investigation, nature, perception, stealth, survival |
| rogue | 4 | acrobatics, athletics, deception, insight, intimidation, investigation, perception, performance, persuasion, sleight of hand, stealth |
| sorcerer | 2 | arcana, deception, insight, intimidation, persuasion, religion |
| warlock | 2 | arcana, deception, history, intimidation, investigation, nature, religion |
| wizard | 2 | arcana, history, insight, investigation, medicine, religion |

#### 2f. Generate Starting Equipment

Assign starting equipment per class. Each PC must have at least 1 equipment item.

#### 2g. Assign Unique ID

Generate a UUID v4 for the PC's `id` field.

#### 2h. Build PC Object

Assemble the complete PC object with all required fields:
- `id` (UUID), `name`, `race`, `class`, `level` (1), `xp` (0)
- `ability_scores` (object with STR/DEX/CON/INT/WIS/CHA)
- `hp_current`, `hp_max`
- `skill_proficiencies` (array), `equipment` (array)
- `spellbook` (array, present only for caster classes)

### Step 3: build_party()

Collect all created PCs into the party array.

- Sort by creation order (index 0 = party leader)
- Verify no duplicate character IDs
- Verify party size matches `party_size` from the action

### Step 4: validate_outcome()

Run the assembled party through `character-creation-party-validation-contract.json`:

- Party size: 1-6 PCs
- All races in the extended race registry
- All classes in the extended class registry
- All ability scores in range 3-20 (with racial modifiers)
- HP calculated correctly: `class_hit_die_max + CON_modifier` at level 1
- All required PC fields present: id, name, race, class, level, xp, ability_scores, hp_current, hp_max, skill_proficiencies, equipment
- Skill proficiencies valid for each PC's class
- Each PC has starting equipment (minimum 1 item)

Return format: `{ valid: boolean, errors: [] }`

If valid, output the party via `character-creation-outcome-contract.json` with `party_valid: true` and `created_at` timestamp.

If invalid, return errors and retry creation for failing PCs (up to 2 retries).

## Example Scenario: 3-PC Party Creation (Fighter, Cleric, Rogue)

### Input Action

```json
{
  "party_size": 3,
  "mode": "wizard",
  "characters": [
    { "name": "Thorin", "race": "dwarf", "class": "fighter", "ability_scores": [16, 12, 14, 10, 13, 8] },
    { "name": "Elara", "race": "human", "class": "cleric", "ability_scores": null },
    { "name": "Arya", "race": "elf", "class": "rogue", "ability_scores": null }
  ]
}
```

### Step 1: validate_action()

- party_size = 3 (valid: 1-6)
- mode = "wizard" (valid enum)
- characters array has 3 entries (matches party_size)
- Thorin: name="Thorin", race="dwarf" (valid), class="fighter" (valid), ability_scores=[16,12,14,10,13,8] (6 ints, 3-18 range)
- Elara: name="Elara", race="human" (valid), class="cleric" (valid), ability_scores=null (will roll)
- Arya: name="Arya", race="elf" (valid), class="rogue" (valid), ability_scores=null (will roll)

Result: PASS

### Step 2: create_character() x 3

**PC 1: Thorin (Dwarf Fighter)**

- Race: dwarf (valid). Racial modifiers: CON +2.
- Class: fighter (valid).
- Ability scores provided: [16, 12, 14, 10, 13, 8] → apply dwarf CON +2:
  - `{ STR: 16, DEX: 12, CON: 16, INT: 10, WIS: 13, CHA: 8 }`
- HP: fighter hit die = d10 (max 10). CON modifier = floor((16-10)/2) = +3. HP = 10 + 3 = **13**.
- Skills: fighter chooses 2 from [acrobatics, animal handling, athletics, history, insight, intimidation, perception, survival] → `["athletics", "intimidation"]`
- Equipment: `["chain mail", "longsword", "shield", "light crossbow", "20 bolts", "dungeoneer's pack"]`
- ID: `b2c3d4e5-f6a7-8901-bcde-f12345678901`

```json
{
  "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
  "name": "Thorin",
  "race": "dwarf",
  "class": "fighter",
  "level": 1,
  "xp": 0,
  "ability_scores": { "STR": 16, "DEX": 12, "CON": 16, "INT": 10, "WIS": 13, "CHA": 8 },
  "hp_current": 13,
  "hp_max": 13,
  "skill_proficiencies": ["athletics", "intimidation"],
  "equipment": ["chain mail", "longsword", "shield", "light crossbow", "20 bolts", "dungeoneer's pack"]
}
```

**PC 2: Elara (Human Cleric)**

- Race: human (valid). Racial modifiers: +1 to all abilities.
- Class: cleric (valid).
- Ability scores null → roll using 4d6_drop_lowest: rolled [13, 10, 12, 10, 15, 11] → apply human +1 all:
  - `{ STR: 14, DEX: 11, CON: 13, INT: 11, WIS: 16, CHA: 12 }`
- HP: cleric hit die = d8 (max 8). CON modifier = floor((13-10)/2) = +1. HP = 8 + 1 = **9**.
- Skills: cleric chooses 2 from [history, insight, medicine, persuasion, religion] → `["insight", "medicine"]`
- Equipment: `["mace", "scale mail", "shield", "light crossbow", "20 bolts", "priest's pack", "holy symbol"]`
- Spellbook (caster): `["sacred flame", "spare the dying", "thaumaturgy", "bless", "cure wounds", "shield of faith"]`
- ID: `c3d4e5f6-a7b8-9012-cdef-123456789012`

```json
{
  "id": "c3d4e5f6-a7b8-9012-cdef-123456789012",
  "name": "Elara",
  "race": "human",
  "class": "cleric",
  "level": 1,
  "xp": 0,
  "ability_scores": { "STR": 14, "DEX": 11, "CON": 13, "INT": 11, "WIS": 16, "CHA": 12 },
  "hp_current": 9,
  "hp_max": 9,
  "skill_proficiencies": ["insight", "medicine"],
  "equipment": ["mace", "scale mail", "shield", "light crossbow", "20 bolts", "priest's pack", "holy symbol"],
  "spellbook": ["sacred flame", "spare the dying", "thaumaturgy", "bless", "cure wounds", "shield of faith"]
}
```

**PC 3: Arya (Elf Rogue)**

- Race: elf (valid). Racial modifiers: DEX +2.
- Class: rogue (valid).
- Ability scores null → roll using 4d6_drop_lowest: rolled [10, 15, 12, 14, 13, 8] → apply elf DEX +2:
  - `{ STR: 10, DEX: 17, CON: 12, INT: 14, WIS: 13, CHA: 8 }`
- HP: rogue hit die = d8 (max 8). CON modifier = floor((12-10)/2) = +1. HP = 8 + 1 = **9**.
- Skills: rogue chooses 4 from [acrobatics, athletics, deception, insight, intimidation, investigation, perception, performance, persuasion, sleight of hand, stealth] → `["acrobatics", "deception", "stealth", "perception"]`
- Equipment: `["rapier", "shortbow", "quiver of 20 arrows", "burglar's pack", "leather armor", "two daggers", "thieves' tools"]`
- ID: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "Arya",
  "race": "elf",
  "class": "rogue",
  "level": 1,
  "xp": 0,
  "ability_scores": { "STR": 10, "DEX": 17, "CON": 12, "INT": 14, "WIS": 13, "CHA": 8 },
  "hp_current": 9,
  "hp_max": 9,
  "skill_proficiencies": ["acrobatics", "deception", "stealth", "perception"],
  "equipment": ["rapier", "shortbow", "quiver of 20 arrows", "burglar's pack", "leather armor", "two daggers", "thieves' tools"]
}
```

### Step 3: build_party()

- Collect 3 PCs in creation order: [Thorin, Elara, Arya]
- Index 0 = Thorin (party leader)
- No duplicate IDs: 3 unique UUIDs confirmed
- Party size = 3 (matches action party_size)

### Step 4: validate_outcome()

| Check | Result |
|-------|--------|
| Party size 1-6 | 3 PCs — PASS |
| All races valid | dwarf, human, elf — PASS |
| All classes valid | fighter, cleric, rogue — PASS |
| Ability scores 3-20 | All scores in range — PASS |
| Thorin HP: 10 + 3 = 13 | hp_max=13 — PASS |
| Elara HP: 8 + 1 = 9 | hp_max=9 — PASS |
| Arya HP: 8 + 1 = 9 | hp_max=9 — PASS |
| Required PC fields present | All 11 fields on all PCs — PASS |
| Skill proficiencies valid | All skills from class lists — PASS |
| Equipment present | All PCs have 6+ items — PASS |

Validation result: `{ valid: true, errors: [] }`

### Output Outcome

```json
{
  "party": [
    { "id": "b2c3d4e5-...", "name": "Thorin", "race": "dwarf", "class": "fighter", "level": 1, "xp": 0, "ability_scores": { "STR": 16, "DEX": 12, "CON": 16, "INT": 10, "WIS": 13, "CHA": 8 }, "hp_current": 13, "hp_max": 13, "skill_proficiencies": ["athletics", "intimidation"], "equipment": ["chain mail", "longsword", "shield", "light crossbow", "20 bolts", "dungeoneer's pack"] },
    { "id": "c3d4e5f6-...", "name": "Elara", "race": "human", "class": "cleric", "level": 1, "xp": 0, "ability_scores": { "STR": 14, "DEX": 11, "CON": 13, "INT": 11, "WIS": 16, "CHA": 12 }, "hp_current": 9, "hp_max": 9, "skill_proficiencies": ["insight", "medicine"], "equipment": ["mace", "scale mail", "shield", "light crossbow", "20 bolts", "priest's pack", "holy symbol"], "spellbook": ["sacred flame", "spare the dying", "thaumaturgy", "bless", "cure wounds", "shield of faith"] },
    { "id": "a1b2c3d4-...", "name": "Arya", "race": "elf", "class": "rogue", "level": 1, "xp": 0, "ability_scores": { "STR": 10, "DEX": 17, "CON": 12, "INT": 14, "WIS": 13, "CHA": 8 }, "hp_current": 9, "hp_max": 9, "skill_proficiencies": ["acrobatics", "deception", "stealth", "perception"], "equipment": ["rapier", "shortbow", "quiver of 20 arrows", "burglar's pack", "leather armor", "two daggers", "thieves' tools"] }
  ],
  "party_valid": true,
  "created_at": "2026-05-27T16:00:00Z"
}
```

The /game-play orchestrator receives this outcome, sets `campaign.party` to the party array, and continues to the campaign loop.
