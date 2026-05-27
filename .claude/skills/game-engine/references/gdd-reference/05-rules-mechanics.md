# 5. Rules/Mechanics — Tiny Civ Reference

## Combat Resolution
**Formula:** `damage = base_damage * (attacker_strength / defender_strength) * modifier_product`

- Both attacker and defender take damage (attacker takes less)
- Ranged units deal damage without taking any in return

## Combat Modifiers

| Modifier | Value | Condition |
|----------|-------|-----------|
| Terrain (hills, forest) | +25% defense | Defender on hill or forest |
| Fortified | +25% defense | Unit skipped turn to fortify |
| City defense | +50% | Defending inside city (+ walls bonus) |
| Flanking | +10% per flanker | Adjacent friendly melee unit |
| Great General | +15% | General within range |
| Health | Proportional | remaining HP / max HP |
| Promotions | Varies | Per promotion type |
| Government | Varies | Per government type |
| Religion belief | Varies | Per belief |

## City Combat
- City combat strength = proportional to population + walls
- Cities bombard 1 enemy unit per turn within range 2
- **Capture sequence:** reduce city HP to 0, then melee attack
- **Post-capture:** annex (unhappy) | puppet (less control) | raze (destroy over turns)

## Zone of Control
- Military units exert ZoC on adjacent tiles
- Enemy units entering a ZoC tile must stop (costs all remaining movement)

## Diplomacy Actions

| Action | Effect | Notes |
|--------|--------|-------|
| Declare War | Open hostilities | Warmonger penalty |
| Peace Treaty | End war | 10-turn enforced peace |
| Open Borders | Units pass through | Mutual agreement |
| Trade Agreement | Exchange resources | Gold, luxuries, strategic |
| Alliance | Shared sight, +10% science, mutual defense | Requires 30+ turns friendship |
| Denounce | Public condemnation | Others may pile on |
| Embassy | See capital, +1 diplomatic visibility | Requires Writing tech |

## Diplomatic Reputation
- Honor deals → +reputation
- Break promise → -reputation
- Surprise war → -major reputation
- Liberate city → +reputation
- Use nukes → -catastrophic reputation
- AI remembers and adjusts behavior accordingly
