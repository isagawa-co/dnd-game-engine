# Configuration Skill — Balance Levers, Player Settings, Campaign Metadata

## Identity

| Key | Value |
|-----|-------|
| Skill | configuration |
| Domain | game-engine |
| Purpose | Configuration-driven game balance, player preferences, and campaign identity |

## Contracts

| Contract | Path | Purpose |
|----------|------|---------|
| Balance Levers | `contracts/balance-levers-contract.json` | Difficulty multipliers, XP curves, treasure scales, encounter settings |
| Player Settings | `contracts/player-settings-contract.json` | Rules complexity, character creation, narration style, death handling |
| Campaign Metadata | `contracts/campaign-metadata-contract.json` | Campaign identity, versioning, content packs, level range, session planning |

## Loading Configuration

Configuration files live in `projects/ai-dnd-game/config/` as JSON files:

| File | Contract | Description |
|------|----------|-------------|
| `balance-levers.json` | balance-levers-contract | Active balance settings for current campaign |
| `player-settings.json` | player-settings-contract | Active player/DM preferences |
| `campaign-metadata.json` | campaign-metadata-contract | Current campaign identity and parameters |

### Load Order

1. Read `campaign-metadata.json` — identifies which campaign and content packs
2. Read `balance-levers.json` — applies difficulty multipliers to all mechanical systems
3. Read `player-settings.json` — applies rules, creation method, narration style

### Validation

Each config file is validated against its contract schema. Validation checks:
- Required fields present
- Enum values match allowed values
- Numeric ranges respected (min/max)
- Cross-field rules (e.g., standard-array requires ability scores array)
- Content pack references exist in catalog (META-002)

## Key Rules

1. **Config-driven mechanics** — All balance adjustments flow from configuration, never hardcoded
2. **Transparent tuning** — Every multiplier and setting is documented with effects
3. **Campaign-constant** — Player settings are set at campaign start and do not change mid-campaign
4. **Balance levers are runtime** — Balance levers CAN be adjusted mid-campaign (e.g., difficulty slider)
5. **Schema validation** — Every config load validates against the contract schema before use

## Anti-Patterns

- Never hardcode difficulty values — use balance-levers.json
- Never assume standard 5e rules — check player-settings.json
- Never skip validation — invalid configs cause silent mechanical errors
- Never modify campaign-metadata mid-session — it's campaign identity

## Downstream Consumers

| Consumer | Uses | Purpose |
|----------|------|---------|
| Combat Loop | balance-levers (difficulty_multiplier, critical_hit_damage) | Scale monster stats, damage |
| Encounter Generator | balance-levers (encounter_difficulty_mode, deadly_threshold) | Select appropriate encounters |
| Loot System | balance-levers (treasure_scale, magic_item_rarity) | Scale treasure drops |
| Character Creation | player-settings (character_creation_method, ability_scores) | Determine stat generation |
| Narration Skill | player-settings (narration_style) | Adjust narrative tone |
| Death System | player-settings (death_handling, resurrection_cost) | Handle character death |
| XP/Leveling | balance-levers (xp_curve) | Calculate XP requirements |
| Campaign Loader | campaign-metadata (content_packs, level_range) | Load correct content |
