# Character Creation Loop — Skill Definition

## Identity

| Key | Value |
|-----|-------|
| Skill | character-creation-loop |
| Type | Sub-loop |
| Parent | /game-play command |
| Purpose | Create a party of PCs when a new campaign has no party, returning a validated party array ready for campaign play |

## Vocabulary

| Term | Definition |
|------|-----------|
| character sheet | Complete PC data structure: ability scores, class, race, proficiencies, equipment, HP, AC |
| party | Array of 1-6 validated PC entities assigned to a campaign |
| PC | Player Character — a Tier 4 entity controlled by the game system |
| leveling | XP-based progression that increases level, grants features, and improves stats |
| multiclass | Taking levels in more than one class (not used during initial creation) |
| creation_method | Algorithm for generating ability scores: point_buy, standard_array, 4d6_drop_lowest, 2d6_plus_6, custom |
| party composition | Balance of martial and caster classes within the party |
| race modifiers | Ability score increases granted by a PC's chosen race |

## Contracts

| Contract | Path | Purpose |
|----------|------|---------|
| Action | → [[contracts/character-creation-action-contract.json]] | Input schema for character creation requests |
| Outcome | → [[contracts/character-creation-outcome-contract.json]] | Output schema for creation results with party data |
| Party Validation | → [[contracts/character-creation-party-validation-contract.json]] | Validation rules for assembled party composition and PC integrity |

## Resolution Flow

1. **Receive character-creation action from /game-play** — orchestrator dispatches to this loop when `campaign.party` is null or empty (state evaluation priority 0 rule)
2. **validate_party_count()** — ensure requested party size is 1-6 PCs (default 3), reject if out of range
3. **create_character()** — for each PC slot: select class/race from content registries, generate ability scores per creation method, assign proficiencies and equipment, build Tier 4 PC entity, validate against CHAR-001 through CHAR-008
4. **build_party()** — collect all validated PCs into array, assign party order (index 0 = leader), verify no duplicate character IDs, validate party composition (at least one martial + one caster)
5. **Return outcome** — output party array and validation status per outcome contract; /game-play sets `campaign.party` from outcome and continues campaign loop

## Integration

| Direction | System | Interface |
|-----------|--------|-----------|
| Called by | /game-play | Dispatched when state evaluation returns `character-creation-loop` (priority 0: party is null/empty) |
| Depends on | Character Skill | `create_character`, `generate_ability_scores`, `validate_character` |
| Depends on | Entity System | Tier 4 PC entity validation |
| Depends on | Configuration | `player-settings.json` for creation method, difficulty, homebrew rules |
| Depends on | Content Registries | `all-races.json`, `all-classes.json` for dynamic race/class data |
| Depends on | Atomic Ops | `dice_roll` for random ability generation methods |
| Returns to | /game-play | Outcome with validated party array; orchestrator sets `campaign.party` and continues |

## Workflow Reference

→ [[character-creation-workflow-reference.md]]

## Rules

1. No Python implementation — this skill is prescriptive instructions for agents
2. Contract-driven — all creation uses action/outcome/validation contract schemas
3. Tier 4 entities — all PCs must be valid Tier 4 entities per entity system
4. Idempotent — if `campaign.party` already exists and is non-empty, skip creation entirely
5. Retry on failure — if a PC fails validation, retry up to 2 times before reporting error
6. Balanced composition — party must include at least one martial and one caster class
7. Registry-driven — class/race validation uses loaded content registries, no hardcoded lists
