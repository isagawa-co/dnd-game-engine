# 19. External Dependencies — Tiny Civ Reference

## Required Libraries

| Dependency | Purpose | Category |
|-----------|---------|----------|
| Simplex noise library | Procedural map generation | Computation |
| Terminal rendering library | ASCII display, color, input handling | Computation |

## Data Files (Built, Not Pulled)
All game data is authored as part of the GDD — no external data sources needed for Tiny Civ. Civilization definitions, tech trees, unit stats, etc. are all original content defined in JSON data files.

## Asset Requirements
- Hand-drawn ASCII character set (original art)
- No external sprite sheets, audio, or fonts required
- Minimal external dependencies by design (ASCII = no asset pipeline)

## Granularity Notes
This is a simple case — Tiny Civ has almost no external dependencies. A sports game (NFL stats), a card game (card databases), or a geography game (map data) would have significant external data requirements. See the External Dependency Resolution principle in the design principles doc for how those cases are handled.
