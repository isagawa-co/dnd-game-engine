# 15. Data Model — Tiny Civ Reference

## Data Files
All game content externalized to data files:

| Data File | Contents | Example Fields |
|-----------|----------|----------------|
| civilizations.json | Civ definitions | name, unique_ability, unique_unit, unique_building, start_bias |
| tech_tree.json | Tech definitions | name, era, cost, prerequisites, unlocks |
| units.json | Unit stats | name, era, cost, strength, movement, range, requires |
| buildings.json | Building stats | name, cost, requires_tech, effects |
| wonders.json | Wonder stats | name, cost, era, effect |
| policies.json | Civic policy trees | tree_name, policies[], effects |
| governments.json | Government types | name, requires_tech, bonuses, penalties |
| pantheons.json | Pantheon options | name, effect |
| beliefs.json | Religion beliefs | name, effect |
| terrain.json | Terrain types | char, food, production, gold, defense_bonus, passable |
| resources.json | Resource definitions | name, category, yield_bonus, required_tech |
| events.json | Random event definitions | name, trigger, effect, conditions |
| promotions.json | Unit promotions | name, xp_required, effect |

## Modding Support
Data-driven design enables balance tuning and content addition without code changes. Users can modify JSON files to:
- Add new civilizations
- Adjust unit balance
- Create custom tech trees
- Define new random events
