# Character — Skill Definition

## Identity

| Key | Value |
|-----|-------|
| Skill | Character |
| Type | Prescriptive |
| Parent | entity |
| Purpose | PC creation, leveling, and ability management |

## Vocabulary

| Term | Definition |
|------|-----------|
| creation_method | Algorithm for generating ability scores: point_buy, standard_array, 4d6_drop_lowest, 2d6_plus_6, custom |
| ability_scores | Six core stats: STR, DEX, CON, INT, WIS, CHA (range 3-20) |
| class | One of 12 D&D 5e character classes determining hit die, features, and proficiencies |
| proficiency_bonus | Level-based bonus (2-6) added to proficient checks and attacks |
| ASI | Ability Score Increase — +2 to ability scores at levels 4, 8, 12, 16, 19 |
| expertise | Doubled proficiency bonus for specific skills (rogue, bard) |
| spell_slots | Per-level resource for casting spells (full/half/warlock casters) |
| hit_dice | Per-level dice pool for healing during short rests |

## Contracts

| Contract | Path | Purpose |
|----------|------|---------|
| Character Creation | `contracts/character-creation-contract.json` | Ability scores, class selection, proficiency assignment, equipment |
| Leveling | `contracts/leveling-contract.json` | XP thresholds, ASI, feature grants, spell slots, hit dice |

## Resolution Flow

### Character Creation

1. **Method Selection** — Read `creation_method` from input (or config `player-settings.json`)
2. **Ability Score Generation** — `generate_ability_scores(method, distribution)`
3. **Class Selection** — `get_class_data(class_name)` for hit die, proficiency pools, features
4. **Proficiency Assignment** — `assign_proficiencies(class_name, chosen_skills)` validates against class pool
5. **Equipment Assignment** — `assign_equipment(class_name, equipment_choice)` returns items + gold
6. **Entity Construction** — Build Tier 4 PC entity dict with all fields
7. **Validation** — `validate_character(character)` checks CHAR-001 through CHAR-008
8. **Output** — Return `{valid, character, errors}`

### Level Up

1. **XP Check** — `check_level_up(current_level, current_xp, xp_gained)` against XP thresholds
2. **HP Gain** — Roll or average hit die + CON modifier (minimum 1)
3. **ASI Check** — `check_asi(new_level)` for levels 4, 8, 12, 16, 19
4. **Feature Grants** — `get_class_features(class_name, new_level)` auto-applied
5. **Spell Slot Update** — `get_spell_slots(class_name, new_level)` for casters
6. **Hit Dice Refresh** — Increment maximum hit dice to match new level
7. **Proficiency Bonus Update** — `calculate_proficiency_bonus(new_level)`
8. **Validation** — Verify LVL-001 through LVL-006
9. **Output** — Return `{leveled_up, new_level, hp_gained, new_features, ...}`

## Integration

| Direction | System | Interface |
|-----------|--------|-----------|
| Depends on | Entity System | Tier 4 validation, `calculate_ability_modifier`, `CLASS_HIT_DICE` |
| Depends on | Configuration | `character_creation_method` from `player-settings.json` |
| Depends on | Atomic Ops | `dice_roll` for random ability generation and HP rolls |
| Used by | Campaign Loop | Party creation, XP awards |
| Used by | Scene Loop | Character checks, combat setup |
| Used by | Game Session | `/game-create` character creation command |
| Produces | Character Pool | Writes to `characters/<id>.json` via `contracts/character-pool-contract.json` |

## Fixtures

| Fixture | Path | Purpose |
|---------|------|---------|
| Fighter PC | `fixtures/fighter-pc.json` | Point-buy fighter, level 1, melee focus |
| Wizard PC | `fixtures/wizard-pc.json` | Standard-array wizard, level 1, spellcaster |
| Rogue PC | `fixtures/rogue-pc.json` | 4d6 rogue, level 1, expertise + 4 skills |

