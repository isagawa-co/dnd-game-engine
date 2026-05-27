# 4. Player Actions — Tiny Civ Reference

## City Management
- **Found city** — Settler consumed on use, minimum 3 tiles from any other city
- **City claims** radius of workable tiles (starts 1-ring, grows with culture)
- **Population** — driven by food surplus, each citizen works one tile
- **Production queue** — build units, buildings, or wonders

### City Stats
| Stat | Source | Purpose |
|------|--------|---------|
| Population | Food surplus fills growth bucket | More citizens = more workable tiles |
| Food | Worked tiles + buildings | Drives population growth |
| Production | Worked tiles + buildings | Speed of building |
| Gold | Worked tiles + buildings + trade | Treasury income |
| Science | Population base + buildings | Research speed |
| Culture | Buildings + wonders + policies | Border expansion, policy unlocks |
| Faith | Buildings + wonders | Religious spread, unit purchases |
| Happiness | Luxuries + buildings - population | Below 0 = unrest |

### Growth
- Food surplus fills growth bucket each turn
- Bucket full → population +1
- Each new citizen increases food requirement (natural cap)
- 0 happiness → growth halts
- Negative happiness → population can decline

## Tile Improvements (built by Workers)

| Improvement | Turns | Requires | Effect |
|-------------|-------|----------|--------|
| Farm | 3 | — | +1 food (+1 with Fertilizer) |
| Mine | 3 | Mining | +1 production (+1 with Chemistry) |
| Road | 1 | Wheel | Faster movement, trade connections |
| Lumber Mill | 3 | Construction | +1 production on forest |
| Plantation | 3 | Calendar | Harvests luxury resource |
| Quarry | 3 | Masonry | +1 production on hills with stone |
| Fishing Boat | 2 | Sailing | +1 food from coast resource |
| Fort | 3 | Engineering | +100% defense |
