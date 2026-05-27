---
name: genre-mapping
type: reference
parent: game-engine
---

# Genre → GDD Section Mapping

Use this matrix to determine which sections apply when a genre is selected during discovery.

**Legend:** ● = Required | ○ = Recommended | — = Skip unless user requests

## Section Applicability Matrix

| # | Section | 4X | Platformer | Puzzle | Card | RPG | Roguelike | Tower Defense | Racing |
|---|---------|-----|-----------|--------|------|-----|-----------|--------------|--------|
| 1 | Game Loop | ● | ● | ● | ● | ● | ● | ● | ● |
| 2 | World/Space | ● | ● | ● | ○ | ● | ● | ● | ● |
| 3 | Entities | ● | ● | ● | ● | ● | ● | ● | ● |
| 4 | Player Actions | ● | ● | ● | ● | ● | ● | ● | ● |
| 5 | Rules/Mechanics | ● | ● | ● | ● | ● | ● | ● | ● |
| 6 | Progression | ● | ● | ○ | ● | ● | ● | ● | ○ |
| 7 | Win/Lose | ● | ● | ● | ● | ● | ● | ● | ● |
| 8 | UI/Rendering | ● | ● | ● | ● | ● | ● | ● | ● |
| 9 | AI/Opponents | ● | ○ | — | ● | ● | ● | ● | ○ |
| 10 | Economy | ● | ○ | — | ○ | ● | ● | ● | — |
| 11 | Randomness | ● | ○ | ○ | ● | ○ | ● | ○ | — |
| 12 | Multiplayer | — | — | — | ○ | — | — | — | ○ |
| 13 | Narrative | ○ | ○ | — | — | ● | ○ | — | — |
| 14 | Audio/Visual | ● | ● | ○ | ○ | ● | ● | ○ | ● |
| 15 | Architecture | ● | ● | ● | ● | ● | ● | ● | ● |
| 16 | Data Model | ● | ● | ● | ● | ● | ● | ● | ● |
| 17 | Configuration | ● | ● | ● | ● | ● | ● | ● | ● |
| 18 | Balance | ● | ● | ○ | ● | ● | ● | ● | ● |
| 19 | Scope/Phases | ● | ● | ● | ● | ● | ● | ● | ● |
| 20 | External Deps | ● | ● | ● | ● | ● | ● | ● | ● |

## Typical Section Counts

| Genre | Required | Recommended | Total typical |
|-------|----------|-------------|---------------|
| 4X Strategy | 18 | 1 | 19 |
| Platformer | 14 | 4 | 16-18 |
| Puzzle | 12 | 3 | 13-15 |
| Card Game | 13 | 3 | 14-16 |
| RPG | 17 | 1 | 18 |
| Roguelike | 17 | 1 | 18 |
| Tower Defense | 15 | 2 | 16-17 |

## Usage

1. Look up genre in the matrix
2. Include all ● sections automatically
3. Suggest ○ sections with "recommended for your genre"
4. Skip — sections unless user specifically requests them
5. User can override any suggestion (add or remove sections)
