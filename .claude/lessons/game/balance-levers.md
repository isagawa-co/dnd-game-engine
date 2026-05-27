# Balance Levers

<!-- Seeded: expert knowledge for game balance configuration -->

## The Problem

Hardcoded balance values (damage multipliers, spawn rates, resource yields) make iteration impossible without code changes. Every "does this feel right?" question requires a code edit, test run, and rebuild.

## Why It Fails

- `damage = hp * 0.75` buried in combat.py — who knows what 0.75 means?
- Changing one value requires finding it, understanding context, modifying, testing
- Non-programmers (game designers, playtesters) can't adjust values
- A/B testing different balance profiles requires code branches

## Correct Approach

**Every tunable value lives in config, never in source code.**

```yaml
# config/balance.yaml
combat:
  base_damage_multiplier: 0.75
  terrain_defense_bonus: 0.25
  flanking_bonus_per_unit: 0.10
  flanking_max_units: 3
economy:
  gold_per_trade_route: 3
  science_per_library: 2
  growth_food_multiplier: 1.0
```

```python
# Source code references config
damage = base * config["combat"]["base_damage_multiplier"]
```

**GDD section 18 (Balance)** should enumerate every balance lever:
- What it controls
- Default value
- Reasonable range
- What happens at extremes

**Gate BUILD-04** verifies: no numeric game constants in source files (grep for hardcoded values).

## Source

GDD template section 18 (Balance/Tuning), gate-contract BUILD-04
