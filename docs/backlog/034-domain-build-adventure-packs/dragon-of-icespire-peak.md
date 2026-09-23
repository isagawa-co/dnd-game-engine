# Dragon of Icespire Peak — Adventure Pack

## Status
NEW

## Location
`workspace:adventures/dragon-of-icespire-peak/`

## What It Does
Populate the DoIP pack (levels 1–7) from training knowledge of the official module. Sword Coast / Phandalin sandbox driven by Falcon's quest board, culminating in the white dragon Cryovain at Icespire Hold. Each act file follows `contracts/adventure-scene-contract.json`.

## Chapters and Acts

### Chapter 1: Phandalin Hub (Level 1)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | Falcon's Quest Board | Arrival in Phandalin, Falcon the Hunter hub, the quest board, townsfolk NPCs, Cryovain flyover warning. |

### Chapter 2: Starting Quests (Levels 1–2)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | Dwarven Excavation | Dwarves Dazlyn/Norbus, ochre jelly, kobolds/orcs, unearthed ruins. |
| II | Umbrage Hill | Adabra Gwynn's windmill; manticore attack (dungeon-lite skirmish). |
| III | Gnomengarde | Gnome warren, mad king Gnerkli, flumphs, mimic hoard. |

### Chapter 3: Follow-up Quests (Levels 3–4)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | Butterskull Ranch | Orcs occupying the ranch; rescue the Anchorites. |
| II | Loggers' Camp | Ankhegs raiding the camp; protect the loggers. |
| III | Mountain's Toe Gold Mine | Cryovain's lair-in-waiting; orcs and the dragon may appear — dungeon mine. |

### Chapter 4: Advanced Quests (Levels 4–6)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | Axeholm | Dwarven fortress-dungeon; wights, ghouls, specter, water trap. Pure dungeon crawl. |
| II | Dragon Barrow | Burial mounds; skeletons, will-o'-wisps; the Hammer of the Dragon (dragon-slayer weapon). |
| III | Woodland Manse | Cult-occupied manor; grick, cultists, druid Falcon lead. |

### Chapter 5: Icespire Hold (Levels 6–7)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | Cryovain's Lair | Icespire Hold fortress; orcs, ogres, and the young white dragon Cryovain. Finale boss. |

## Monster References (populate `adventures/dragon-of-icespire-peak/monsters/`)
young-white-dragon (Cryovain), orc, ogre, kobold, ochre-jelly, manticore, flumph, mimic, ankheg, wight, ghoul, specter, skeleton, will-o-wisp, grick, cultist, giant-goat, brown-bear, stirge. (Reuse LMoP stat blocks where identical; add new ones.)

## Transitions
Sandbox — each quest act returns to `chapter-1-phandalin-hub` (quest board) until Cryovain is confronted. `default` from chapter-5-act-I → adventure complete.

## Dependencies
- adventure-scene-contract (schema)
- manifest.json + monsters/ built before/with act files
