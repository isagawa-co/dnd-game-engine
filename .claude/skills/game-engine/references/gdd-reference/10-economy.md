# 10. Economy/Resources — Tiny Civ Reference

## Resources

### Bonus Resources
Wheat, Fish, Deer, Cattle — add extra yield to tile

### Strategic Resources
Iron, Horses, Coal, Oil — required for certain units/buildings. Tech-gated visibility (e.g., Iron Working reveals Iron).

### Luxury Resources
Gold, Gems, Spices, Silk, Wine, Dyes — provide happiness, tradeable.

## Trade Routes
- Established by Trader units between two cities
- Yield gold (based on distance and city size), trickle science/faith
- Domestic routes: food + production transfer
- International routes: gold
- Max routes: 1 base + 1 per harbor/market
- Routes spread religion passively

## Happiness System
```
Happiness = (unique luxury types × 4)
           + building bonuses
           + policy bonuses
           - total population
           - (number of cities × 3)
           - war weariness
```

### Effects by Level

| Level | Name | Effect |
|-------|------|--------|
| 10+ | Golden Age | +20% production, gold, culture |
| 1–9 | Content | Normal operations |
| 0 | Stagnant | No growth |
| -1 to -9 | Unhappy | -25% yields, no settlers |
| -10 | Revolt | Rebel units spawn, cities may flip |

## Great People
Earned by accumulating specialist points from buildings:

| Great Person | Source | Actions |
|-------------|--------|---------|
| Great Scientist | Libraries, Universities | Instant tech boost OR plant Academy (+4 science tile) |
| Great Engineer | Workshops, Factories | Rush-build wonder OR plant Manufactory (+4 production tile) |
| Great Merchant | Markets, Banks | Gold burst OR plant Customs House (+4 gold tile) |
| Great General | Combat | +15% combat nearby OR plant Citadel |
| Great Prophet | Faith | Found/enhance religion OR plant Holy Site (+4 faith tile) |
| Great Artist | Theaters | Culture burst OR plant Landmark (+4 culture tile) |
