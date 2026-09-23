# Forge of Fury — Adventure Pack

## Status
NEW

## Location
`workspace:adventures/forge-of-fury/`

## What It Does
Populate the Forge of Fury pack (levels 3–5) from training knowledge of the classic module. A single site — Khundrukar, the lost stronghold of the smith Durgeddin the Black — descending through four dungeon levels to the young black dragon Nightscale. Pure dungeon crawl. Each act file follows `contracts/adventure-scene-contract.json`.

## Chapters and Acts

### Chapter 1: The Mountain Door (Level 3)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | The Gatehouse | Cliff approach, arrow slits, orc sentries, crank-operated portcullis trap. |
| II | The Great Hall | Orc warband under Great Ulfe (half-ogre), Grula-Munfsh, war dogs; trophy hall. |

### Chapter 2: The Glitterhame (Level 3–4)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | The Caverns | Natural caverns, troglodytes, stirges, mushroom cave, silver vein, glowing crystals. |
| II | The Black Lake Shore | Underground lake edge, Nightscale's lair proximity, troglodyte shaman, hidden stair to the Foundry. |

### Chapter 3: The Foundry (Level 4)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | Durgeddin's Forge | Duergar occupants, the smithy, roper in the flooded gallery, quenching pools. |
| II | The Vault & Ghosts | Grimlocks, Durgeddin's masterwork blades (Nightfang etc.), spectral dwarf guardians, secret vault. |

### Chapter 4: Black Lake (Level 5)
| Act | Title | Key Content |
|-----|-------|-------------|
| I | Nightscale's Lair | The young black dragon Nightscale in the flooded lower cavern; submerged hoard, final boss. |

## Monster References (populate `adventures/forge-of-fury/monsters/`)
young-black-dragon (Nightscale), orc, half-ogre (Great Ulfe), orc-war-dog, troglodyte, stirge, duergar, roper, grimlock, specter (dwarf ghosts), giant-rat, dark-mantle. (Reuse LMoP stat blocks where identical; add new ones.)

## Transitions
Linear descent: each act's `default` → next act, chapter-4-act-I → adventure complete. `retreat_to_surface` transitions back up a level for rest.

## Dependencies
- adventure-scene-contract (schema)
- manifest.json + monsters/ built before/with act files
