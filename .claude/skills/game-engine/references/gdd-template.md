---
name: gdd-template
type: reference
parent: game-engine
---

# GDD Template Sections (Generalized)

Every game must answer these questions. Discovery determines depth per section.

## Core (required for all games)
1. **Game Loop** — what happens each tick/turn/frame? What's the core cycle the player repeats?
2. **World/Space** — where does gameplay happen? (map, board, screen, level, arena, grid)
3. **Entities** — what exists in the world? (players, enemies, objects, NPCs, cards, pieces)
4. **Player Actions** — what can the player do? (move, build, shoot, place, select, combine)
5. **Rules/Mechanics** — what governs interactions? (physics, combat, scoring, matching, economy)
6. **Progression** — how does the game advance? (levels, tech tree, unlocks, difficulty curve, story)
7. **Win/Lose Conditions** — how does it end? (victory, defeat, score, survival, completion)
8. **UI/Rendering** — how does the player see and interact? (HUD, menus, controls, camera, input)

## Systems (genre-dependent, discovered in Phase 1)
9. **AI/Opponents** — who/what opposes the player? (enemy AI, NPC behavior, difficulty scaling)
10. **Economy/Resources** — what does the player collect, spend, manage? (currency, mana, ammo, inventory)
11. **Randomness/Procedural** — what varies between playthroughs? (map gen, loot tables, events)
12. **Multiplayer/Social** — how do players interact? (co-op, PvP, trade, chat, leaderboards)
13. **Narrative/Lore** — what's the story context? (dialogue, quests, history, world-building)
14. **Audio/Visual Style** — what's the aesthetic? (art direction, music, sound design, effects)

## Infrastructure (required for all games)
15. **Technical Architecture** — what systems exist in code? (ECS, scene graph, state machine, data flow)
16. **Data Model** — what's stored and how? (save format, config files, data-driven content)
17. **Configuration** — what's tunable? (difficulty, controls, display, accessibility)
18. **Balance Levers** — what knobs control fun? (damage curves, spawn rates, resource yields, pacing)
19. **Scope/Phases** — what's built first? (MVP, dependencies, phase ordering)
20. **External Dependencies** — what's pulled, not built? (MCPs, APIs, packages, assets, datasets)

## Genre Mapping

| Section | 4X Strategy | Platformer | Puzzle | Card Game | RPG |
|---------|------------|------------|--------|-----------|-----|
| World/Space | hex map, fog | side-scroll levels | grid/board | table/hand | overworld + dungeons |
| Entities | units, cities, civs | player, enemies, items | pieces, blocks | cards, decks | party, NPCs, monsters |
| Rules/Mechanics | combat, diplomacy, trade | physics, collision | matching, chain | draw, play, discard | combat, stats, spells |
| AI/Opponents | civ AI personalities | enemy patterns | hint system | opponent AI | encounter AI |
| Economy | gold, science, faith | coins, lives | score, stars | mana, dust | gold, XP, loot |
| Progression | tech tree, eras | world map, boss gates | level packs | ranked ladder | leveling, skill trees |
