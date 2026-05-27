# Character Creation Loop — Skill

Prescriptive workflow for creating a party of PCs when a new campaign has no party. Invoked by the orchestrator when state evaluation returns `character-creation-loop` (priority 0 rule).

## Contracts Referenced

| Contract | Path | Purpose |
|----------|------|---------|
| Character Creation | `.claude/skills/character/contracts/character-creation-contract.json` | Input/output schema for PC creation, validation rules CHAR-001 through CHAR-008 |
| Player Settings | `projects/ai-dnd-game/config/player-settings.json` | Creation method, house rules, difficulty |
| State Evaluation | `projects/ai-dnd-game/contracts/state-evaluation-contract.json` | Priority 0 rule triggers this loop |

## Dependencies

| System | Module | Key Functions |
|--------|--------|---------------|
| Character Skill | `projects/ai-dnd-game/src/entity/character_creator.py` | `create_character`, `generate_ability_scores`, `get_class_data`, `assign_proficiencies`, `assign_equipment`, `validate_character` |
| Entity System | `projects/ai-dnd-game/src/entity/entity_loader.py` | Tier 4 PC entity validation |
| Atomic Ops | `.claude/skills/atomic_ops/` | `dice_roll` for random ability generation methods |
| Race Registry | `projects/ai-dnd-game/content/all-races.json` | Dynamic race data with ability modifiers |
| Class Registry | `projects/ai-dnd-game/content/all-classes.json` | Dynamic class data with hit dice, features |

## Instructions

### Part 0: Load Registries

**This step runs BEFORE any character creation. It loads the dynamic registries that replace all hardcoded class/race lists.**

1. Load race registry from `projects/ai-dnd-game/content/all-races.json`:
   - Parse JSON, extract `races` array
   - Build lookup map: `race_registry = {r["id"]: r for r in data["races"]}`
   - Extract available race IDs: `valid_race_ids = set(race_registry.keys())`
   - If file missing or invalid JSON: STOP with error `"Registry load failed: all-races.json not found or invalid. Cannot create characters without race registry."`

2. Load class registry from `projects/ai-dnd-game/content/all-classes.json`:
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

### Part 3: Party Assembly

1. Collect all created PC entities into `campaign.party` array
2. Assign party order (index 0 = party leader, typically highest CHA)
3. Validate party composition:
   - Party size matches configured count
   - All PCs are valid Tier 4 entities (`entity_type: "pc"`, `level: 1`)
   - No duplicate character IDs
4. Build party roster summary: name, class, HP, AC for each PC

### Part 4: Equipment and Gold

1. Calculate starting gold per PC based on class and `campaign_difficulty`:
   - Standard gold per `character-creation-contract.json` class defaults
   - Adjust for difficulty: easy (+50%), intermediate (standard), hard (-25%)
2. Verify equipment assignments per CHAR-007 (weight limit: STR * 15)
3. Build inventory array for each PC from equipment choices
4. Add gold to each PC's `gold` field

### Part 5: Save to Campaign

1. Write updated campaign state with `party` array populated:
   - Update `campaigns/<campaign-id>/campaign_state.json`
   - Set `campaign.party` to array of PC entity objects
2. Create `campaigns/<campaign-id>/party.json`:
   - Contains party roster with all PC data
   - Includes creation metadata (method, timestamp)
3. Validate save per game-session save contract (atomic write, checksum)
4. Report success:
   ```
   Party created — [N] PCs ready for adventure.

   | # | Name | Class | HP | AC |
   |---|------|-------|----|----|
   | 1 | [name] | [class] | [hp] | [ac] |
   | 2 | [name] | [class] | [hp] | [ac] |
   | 3 | [name] | [class] | [hp] | [ac] |
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
