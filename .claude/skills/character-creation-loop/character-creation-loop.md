# Character Creation Loop — Skill

Prescriptive workflow for creating a party of PCs when a new campaign has no party. Invoked by the orchestrator when state evaluation returns `character-creation-loop` (priority 0 rule).

## Contracts Referenced

| Contract | Path | Purpose |
|----------|------|---------|
| Character Creation | `.claude/skills/character/contracts/character-creation-contract.json` | Input/output schema for PC creation, validation rules CHAR-001 through CHAR-008 |
| Player Settings | `config/player-settings.json` | Creation method, house rules, difficulty |
| State Evaluation | `contracts/state-evaluation-contract.json` | Priority 0 rule triggers this loop |

## Dependencies

| System | Module | Key Functions |
|--------|--------|---------------|
| Character Skill | `src/entity/character_creator.py` | `create_character`, `generate_ability_scores`, `get_class_data`, `assign_proficiencies`, `assign_equipment`, `validate_character` |
| Entity System | `src/entity/entity_loader.py` | Tier 4 PC entity validation |
| Atomic Ops | `.claude/skills/atomic_ops/` | `dice_roll` for random ability generation methods |
| Race Registry | `adventures/all-races.json` | Dynamic race data with ability modifiers |
| Class Registry | `adventures/all-classes.json` | Dynamic class data with hit dice, features |

## Instructions

### Part 0: Load Registries

**This step runs BEFORE any character creation. It loads the dynamic registries that replace all hardcoded class/race lists.**

1. Load race registry from `adventures/all-races.json`:
   - Parse JSON, extract `races` array
   - Build lookup map: `race_registry = {r["id"]: r for r in data["races"]}`
   - Extract available race IDs: `valid_race_ids = set(race_registry.keys())`
   - If file missing or invalid JSON: STOP with error `"Registry load failed: all-races.json not found or invalid. Cannot create characters without race registry."`

2. Load class registry from `adventures/all-classes.json`:
   - Parse JSON, extract `classes` array
   - Build lookup map: `class_registry = {c["id"]: c for c in data["classes"]}`
   - Extract available class IDs: `valid_class_ids = set(class_registry.keys())`
   - If file missing or invalid JSON: STOP with error `"Registry load failed: all-classes.json not found or invalid. Cannot create characters without class registry."`

3. Derive composition categories from registry data (no hardcoded lists):
   - `caster_ids = {id for id, c in class_registry.items() if "spellcasting" in c or "spell_slots_by_level" in c}`
   - `martial_ids = {id for id, c in class_registry.items() if id not in caster_ids}`
   - Classification is purely data-driven: classes with a `spellcasting` key are casters, all others are martial
   - These sets are used for party composition validation in Part 2 and Part 3

4. Log registry load summary:
   ```
   Registries loaded: [N] races, [M] classes
   Sources: [list of source books from registry metadata]
   ```

### Part 1: Party Configuration

1. Read `player-settings.json` to determine:
   - `character_creation_method` — one of: `point_buy`, `standard_array`, `4d6_drop_lowest`, `2d6_plus_6`, `custom`
   - `campaign_difficulty` — affects starting equipment and gold
   - `homebrew_content_allowed` — if false, restricts class/race options to PHB source only
2. Determine party size: 3 PCs (default), configurable via campaign metadata
3. Check campaign directory for pre-built PC fixtures:
   - If fixtures exist in `campaigns/<campaign-id>/fixtures/`: load them instead of creating
   - If no fixtures: proceed to Part 2
4. Build creation plan: list of PC slots with assigned classes (balanced party composition)
   - Select classes from `valid_class_ids` (loaded in Part 0), not hardcoded lists
   - If `homebrew_content_allowed` is false: filter to classes/races where `source == "PHB"` only

### Part 2: Character Creation Per PC

For each PC slot (repeat for party size):

1. **Select class** — ensure party balance using registry-derived categories:
   - At least one class from `martial_ids` (loaded in Part 0)
   - At least one class from `caster_ids` (loaded in Part 0)
   - Validate selected class ID exists in `valid_class_ids` — reject if not found in registry
   - No duplicate classes unless party size > 4
2. **Select race** — validate against registry:
   - Validate selected race ID exists in `valid_race_ids` — reject if not found in registry
   - Load race data from `race_registry[race_id]` for ability modifiers
3. **Generate ability scores** — invoke `generate_ability_scores(method, distribution)`:
   - Method from `player-settings.json` `character_creation_method`
   - Distribution optimized for chosen class (e.g., fighter prioritizes STR/CON)
4. **Apply race ability modifiers** — from registry data:
   - Load `ability_score_increases` from `race_registry[race_id]`
   - Apply each modifier to the generated base scores: `score[ability] += modifier`
   - Example: if race entry has `"ability_score_increases": {"con": 2, "wis": 1}`, add +2 CON, +1 WIS
   - Validate final scores still pass CHAR-001 (3-20 range) after applying modifiers
5. **Assign proficiencies** — invoke `assign_proficiencies(class_name, chosen_skills)`:
   - Load class skill pool from `class_registry[class_id]` or fallback to `character-creation-contract.json` `class_data`
   - Respect `skill_count` limit per class from registry
6. **Assign equipment** — invoke `assign_equipment(class_name, equipment_choice)`:
   - Default to `option_a` unless campaign specifies otherwise
7. **Build PC entity** — invoke `create_character(input)` with full input per contract `input_schema`:
   - `name`, `class`, `creation_method`, `ability_input`, `chosen_skills`, `equipment_choice`, `race`, `background`
   - `class` and `race` must be valid IDs from their respective registries
8. **Validate** — invoke `validate_character(character)`:
   - Must pass CHAR-001 through CHAR-008 from `character-creation-contract.json`
   - If validation fails: log errors, retry with corrected input (max 2 retries)
9. **Output** — collect `{valid: true, character: <Tier 4 entity>, errors: []}` for assembly

### Part 3: Personality and Roleplay

For each PC (after mechanical creation in Part 2):

#### Presentation Format (MANDATORY)

Every table in Part 3 MUST be presented using this exact format. This ensures consistent HITL experience across all sessions.

```
Part 3: Personality and Roleplay — PC [N]: [Name] ([Race] [Class])

[Name]'s background is [Background]. Here are the D&D 5e [Background] background options:

[Category] (pick [N] or roll d[die]):

| # | [Column Header] |
|---|-----------------|
| 1 | [option text]   |
| 2 | [option text]   |
| ...               |

Pick [N], roll d[die], or "roll all" to randomize everything.
```

Rules:
- Always show the full table even if player chose "roll" — they see what they got
- One table at a time — wait for player response before showing the next
- After each selection/roll, confirm: "[Name]'s [category]: [selected text]"
- For "roll all": present all tables at once, player provides all rolls, agent maps results

#### Steps

0. **Choose method** — ask the player:
   - **Pick**: player selects each trait from the background table by number
   - **Roll**: player rolls dice, agent maps result to table entry
   - **Roll all**: player rolls d8, d8, d6, d6, d6 — agent maps all at once
   - Present method choice BEFORE showing any tables

1. **Select background** — if not already chosen in Part 2:
   - Background determines personality trait options, ideal options, bond options, flaw options
   - Common backgrounds: acolyte, charlatan, criminal, entertainer, folk hero, guild artisan, hermit, noble, outlander, sage, sailor, soldier, urchin

2. **Personality traits** (2) — pick or roll (d8) from background table:
   - These describe how the character behaves day-to-day
   - Present numbered table of 8 options from background
   - If rolling: player rolls d8 twice (reroll duplicates)

3. **Ideal** (1) — pick or roll (d6) from background table:
   - What principle drives the character
   - Tied to alignment (good, evil, lawful, chaotic, neutral, any)
   - Present numbered table of 6 options from background

4. **Bond** (1) — pick or roll (d6) from background table:
   - A connection to a person, place, or event that matters deeply
   - Present numbered table of 6 options from background

5. **Flaw** (1) — pick or roll (d6) from background table:
   - A weakness, vice, or fear the character struggles with
   - Present numbered table of 6 options from background

6. **Appearance** — brief physical description:
   - Agent proposes based on race/class/background, player can modify
   - Height, build, distinguishing features
   - Useful for narration skill to describe the character in scenes

7. **Backstory** (optional) — 2-3 sentences of character history:
   - Agent proposes based on background/bond/ideal, player can modify or skip
   - Where they came from, why they adventure

8. **Populate fields** — write to character entity:
   - `personality.traits`: array of 2 strings
   - `personality.ideal`: string
   - `personality.bond`: string
   - `personality.flaw`: string
   - `personality.appearance`: string
   - `personality.backstory`: string (optional)
   - `personality.alignment`: already set
   - `personality.background`: already set

### Part 4: Party Assembly

1. Collect all created PC entity IDs into party reference list
2. Assign party order (index 0 = party leader, typically highest CHA)
3. Validate party composition:
   - Party size matches configured count
   - All PCs are valid Tier 4 entities (`entity_type: "pc"`, `level: 1`)
   - No duplicate character IDs
4. Build party roster summary: name, class, HP, AC for each PC

### Part 5: Equipment and Gold

1. Calculate starting gold per PC based on class and `campaign_difficulty`:
   - Standard gold per `character-creation-contract.json` class defaults
   - Adjust for difficulty: easy (+50%), intermediate (standard), hard (-25%)
2. Verify equipment assignments per CHAR-007 (weight limit: STR * 15)
3. Build inventory array for each PC from equipment choices
4. Add gold to each PC's `gold` field

### Part 6: Save to Character Pool and Campaign

1. Save each PC entity to the shared character pool:
   - Write `characters/<character-id>.json` with full Tier 4 entity
   - Include `creation_metadata`: `{ creation_method, created_date, source_campaign }`
   - Include `campaign_history`: `[{ campaign_id, joined_at_level, current_level, status }]`
   - Character ID format: `<name-kebab>-<race>-<class>` (e.g., `honu-tortle-fighter`)
   - Validate against `contracts/character-pool-contract.json`
2. Update campaign with character references (not full entities):
   - Write `campaigns/<campaign-id>/party.json` with character ID references per campaign_reference_schema
   - Each entry: `{ character_id, party_position, snapshot_level, joined_date }`
3. Update `campaigns/<campaign-id>/campaign_state.json`:
   - Set `campaign.party` to array of character IDs (e.g., `["honu-tortle-fighter"]`)
4. Validate save per game-session save contract (atomic write, checksum)
5. Report success:
   ```
   Party created — [N] PCs ready for adventure.
   Characters saved to characters/ pool.

   | # | Name | Class | HP | AC | Character ID |
   |---|------|-------|----|----|--------------|
   | 1 | [name] | [class] | [hp] | [ac] | [character-id] |
   | 2 | [name] | [class] | [hp] | [ac] | [character-id] |
   | 3 | [name] | [class] | [hp] | [ac] | [character-id] |
   ```

## Rules

1. **No Python code** — this skill is prescriptive instructions for agents, not executable code
2. **Contract-driven** — all creation uses `character-creation-contract.json` schemas and validation rules
3. **Tier 4 entities** — all PCs must be valid Tier 4 entities per entity system validation
4. **Idempotent** — if party already exists (`campaign.party != null && campaign.party.length > 0`), skip creation entirely
5. **Retry on failure** — if a PC fails validation, retry up to 2 times before reporting error
6. **Balanced composition** — party must include at least one martial and one caster class (categories derived from registry, not hardcoded)
7. **Registry-driven** — all class and race validation uses loaded registries from `all-races.json` and `all-classes.json`. No hardcoded class or race lists in any validation logic

## Error Handling

| Error | Action |
|-------|--------|
| Race registry not found (`all-races.json` missing) | STOP — cannot create characters without race registry. Report: `"Registry load failed: all-races.json not found"` |
| Class registry not found (`all-classes.json` missing) | STOP — cannot create characters without class registry. Report: `"Registry load failed: all-classes.json not found"` |
| Registry JSON invalid (parse error) | STOP — report parse error details, do not fall back to hardcoded data |
| Race ID not in registry | Reject selection, prompt for valid race from `valid_race_ids` |
| Class ID not in registry | Reject selection, prompt for valid class from `valid_class_ids` |
| Player settings not found | Use defaults: `point_buy`, `intermediate`, no homebrew |
| Ability score validation fails (CHAR-001) | Regenerate scores with same method |
| Ability score out of range after race modifiers | Cap at 20, floor at 3 per CHAR-001 |
| Skill proficiency invalid (CHAR-004) | Select alternative from class pool (loaded from registry) |
| Equipment overweight (CHAR-007) | Remove heaviest item, add lighter alternative |
| All retries exhausted | Log error, report which PC failed, stop creation |
| Campaign state write fails | Retry atomic write once, then report save error |
