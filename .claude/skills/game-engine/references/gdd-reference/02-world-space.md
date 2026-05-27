# 2. World/Space — Tiny Civ Reference

## Terrain Tiles
Hand-drawn ASCII characters on a grid. Two layers:
- **Terrain layer** — land, water, natural features
- **Entity layer** — units, cities, improvements

### Terrain Types and Yields

| Terrain | Char | Food | Prod | Gold | Notes |
|---------|------|------|------|------|-------|
| Plains | `.` | 2 | 1 | 0 | Baseline tile |
| Grassland | `,` | 3 | 0 | 0 | High food for growth |
| Hills | `^` | 1 | 2 | 0 | +25% defensive bonus |
| Mountain | `▲` | 0 | 0 | 0 | Impassable, blocks sight |
| Forest | `♣` | 1 | 2 | 0 | +25% defense, choppable |
| Desert | `~` | 0 | 0 | 0 | Barren unless irrigated |
| Tundra | `_` | 1 | 0 | 0 | Cold, low yield |
| Coast | `≈` | 1 | 0 | 1 | Fishable |
| Ocean | `░` | 0 | 0 | 0 | Requires Sailing tech |
| River | `~` | +1 | 0 | +1 | Overlay on other terrain |

## Resources
Three categories:
- **Bonus** (Wheat, Fish, Deer, Cattle) — extra yield
- **Strategic** (Iron, Horses, Coal, Oil) — required for units/buildings, tech-gated visibility
- **Luxury** (Gold, Gems, Spices, Silk, Wine, Dyes) — happiness, tradeable

## Fog of War
Three states per tile:
- **Unexplored** — solid black, nothing known
- **Revealed** — dimmed, terrain visible, entities not updated
- **Visible** — full brightness, real-time info, within sight range

Sight range varies by unit type and terrain (hills grant +1 sight).

## Map Generation
- Procedural generation using simplex noise
- Configurable: map size (tiny/small/standard), water level, resource density
- Guaranteed fair starts: each civ gets similar access to fresh water, resources, space
