# 9. AI/Opponents — Tiny Civ Reference

## AI Personalities
Behavior driven by weighted priorities, each scored 0–10:

| Dimension | Description |
|-----------|-------------|
| Aggression | Likelihood to build military, declare war |
| Expansion | Priority on settling new cities |
| Science | Research focus |
| Diplomacy | Willingness to trade, make deals |
| Faith | Religious focus |
| Culture | Wonder/culture priority |
| Loyalty | How reliably they honor agreements |

## Preset Personalities

| Personality | Aggr | Exp | Sci | Dipl | Faith | Cult | Loyalty |
|-------------|------|-----|-----|------|-------|------|---------|
| Warlord | 9 | 7 | — | 2 | — | — | — |
| Scholar | 2 | — | 9 | — | — | 6 | — |
| Merchant | — | 6 | — | 8 | — | — | — |
| Prophet | — | — | — | 5 | 9 | 7 | — |
| Pacifist | 1 | — | — | 9 | — | 7 | — |

## Decision Making
Simple utility system: each possible action scored by weighted priorities, highest score wins.

## Barbarians
- Spawn in camps in unclaimed/unexplored territory
- Scout first, then spawn combat units
- Attack any nearby civ units and cities
- Camps cleared for gold reward
- Difficulty scales with game era (stronger units)
