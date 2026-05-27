# 11. Randomness/Procedural — Tiny Civ Reference

## Map Generation
- Procedural generation using simplex noise
- Configurable: map size (tiny/small/standard), water level, resource density
- Guaranteed fair starts: each civ gets similar access to fresh water, resources, space

## Random World Events

| Event | Effect |
|-------|--------|
| Barbarian uprising | Barbarian camp spawns in unclaimed territory |
| Natural disaster | Flood/earthquake damages improvements in area |
| Golden age | Civ with highest happiness gets +20% all yields for 10 turns |
| Plague | Cities lose 1 pop if no hospital |
| Resource discovery | New resource appears on a revealed tile |

## Resource Placement
- Resources placed on terrain tiles during map generation
- Bonus resources visible immediately
- Strategic resources hidden until tech reveals them
- Luxury resources visible on discovery
