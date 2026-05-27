# 14. Technical Architecture — Tiny Civ Reference

## Core Systems (16)

| System | Responsibility |
|--------|---------------|
| MapSystem | Terrain generation, fog of war, pathfinding |
| CitySystem | Growth, production, building, yields |
| UnitSystem | Movement, combat, promotions, orders |
| TechSystem | Research queue, tech unlocks |
| CivicSystem | Culture, policies, governments |
| ReligionSystem | Faith, pantheons, beliefs, spread |
| DiplomacySystem | Relations, treaties, trade, reputation |
| TradeSystem | Trade routes, yields, route management |
| AISystem | Decision-making, personality-driven priorities |
| CombatSystem | Damage calculation, modifiers, sieges |
| EventSystem | Random events, history logging |
| HappinessSystem | Global happiness, golden ages, revolts |
| VictorySystem | Condition tracking, win detection |
| RenderSystem | ASCII rendering, layers, UI panels |
| InputSystem | Keyboard handling, command mapping |
| TurnSystem | Turn resolution, phase ordering |

## Data-Driven Design
All game content defined in data files (not hardcoded):
- Civilization definitions
- Tech tree
- Unit stats
- Building stats
- Civic policies
- Religion beliefs and pantheons
- Random event definitions
- Terrain types and yields

This allows modding and easy balance tuning without code changes.
