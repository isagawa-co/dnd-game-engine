# LMoP Adventure Build

## Status
NEW

## Location
`workspace:adventures/lmop/scenes/`

## What It Does
Populate all LMoP chapter act files using agent training knowledge of the official module. Each act file follows the adventure-scene-contract schema.

## Chapters and Acts

### Chapter 1: Goblin Arrows (Level 1)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | The Road to Phandalin | Hook: Gundren hires party. Wagon escort. Travel narration. |
| II | Goblin Ambush | 4 goblins, surprise rules, dead horses, trail to hideout |
| III | Cragmaw Hideout | Multi-room dungeon. ~20 goblins, 3 wolves, Klarg (bugbear). Rescue Sildar. Flood trap. |

### Chapter 2: Phandalin (Level 2)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | Welcome to Phandalin | Town arrival, NPC introductions, quest board. Barthen's Provisions, Stonehill Inn, Shrine of Luck. |
| II | The Redbrand Threat | Redbrand confrontation in town. Halia's quest. Townsmaster Harbin's quest. |
| III | Tresendar Manor | Redbrand hideout dungeon. Nothic, Glasstaff (Iarno Albrek), prisoners, secret passage. |

### Chapter 3: The Spider's Web (Level 3)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | Side Quests | Agatha's Lair (banshee), Old Owl Well (necromancer + zombies), Thundertree (dragon + cultists + ash zombies), Wyvern Tor (orcs) |
| II | Cragmaw Castle | King Grol (bugbear), hobgoblins, goblins, owlbear. Rescue Gundren. Get map to Wave Echo Cave. |

### Chapter 4: Wave Echo Cave (Levels 4-5)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | The Outer Caves | Entrance pit, mine tunnels (ochre jelly), old entrance (stirges), guardroom (skeletons) |
| II | The Inner Caves | Great cavern (ghouls), dark pool, barracks (bugbears), smelter (zombies + flameskull), Mormesk the wraith |
| III | The Forge of Spells | Spectator guardian, Forge of Spells, Nezznar the Black Spider (drow) + giant spiders. Final boss. |

## Monster References
All monster_id values reference stat blocks in `adventures/lmop/monsters/`:
goblin, hobgoblin, bugbear, wolf, dire-wolf, orc, skeleton, zombie, nothic, owlbear, giant-spider, stirge, giant-rat, ochre-jelly, rust-monster, redbrand-ruffian, redbrand-mage, king-grol, iarno-albrek, sildar-hallwinter, gundren-rockseeker, drow, black-bear

## Dependencies
- folder-restructure (adventures/lmop/scenes/ must exist)
- adventure-scene-contract (act files must follow schema)
