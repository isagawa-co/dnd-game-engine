# 1. Game Loop — Tiny Civ Reference

## Core Cycle
Explore → Expand → Exploit → Exterminate (4X)

- **Explore:** Scout the map, reveal terrain, find resources
- **Expand:** Found new cities, claim territory
- **Exploit:** Build improvements, research tech, trade
- **Exterminate:** Conquer enemies, win the game

## Turn Structure
1. **Start of turn** — income, research, culture, faith ticked
2. **Player issues orders** — move units, manage cities, diplomacy
3. **AI civilizations take their turns** — simultaneous resolution
4. **End of turn** — growth, production, maintenance applied

## Granularity Notes
This section defines the heartbeat of the game. Every other system plugs into this loop. The turn structure tells you exactly when each system fires — income at start, orders in middle, resolution at end. A developer can implement this without ambiguity.
