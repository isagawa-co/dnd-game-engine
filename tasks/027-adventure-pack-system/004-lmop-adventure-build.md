# Task 004: LMoP Adventure Build

## Type
BUILD

## Goal
Create all act files for Lost Mine of Phandelver chapters 1-4 under `adventures/lmop/scenes/`.

## Act Files to Create
### Chapter 1: Goblin Arrows
- `chapter-1-goblin-arrows/act-I.json` — The road, hook, wagon escort
- `chapter-1-goblin-arrows/act-II.json` — Goblin ambush (4 goblins)
- `chapter-1-goblin-arrows/act-III.json` — Cragmaw Hideout dungeon

### Chapter 2: Phandalin
- `chapter-2-phandalin/act-I.json` — Town arrival, NPC introductions, quests
- `chapter-2-phandalin/act-II.json` — Redbrand confrontation
- `chapter-2-phandalin/act-III.json` — Tresendar Manor dungeon

### Chapter 3: The Spider's Web
- `chapter-3-spiders-web/act-I.json` — Side quests (Agatha, Old Owl Well, Thundertree, Wyvern Tor)
- `chapter-3-spiders-web/act-II.json` — Cragmaw Castle, rescue Gundren

### Chapter 4: Wave Echo Cave
- `chapter-4-wave-echo-cave/act-I.json` — Outer caves
- `chapter-4-wave-echo-cave/act-II.json` — Inner caves
- `chapter-4-wave-echo-cave/act-III.json` — Forge of Spells, Black Spider

## Verification
- 11 act files exist
- All follow adventure-scene-contract schema
- All monster_ids reference existing stat blocks in adventures/lmop/monsters/
- Transitions chain correctly between acts
