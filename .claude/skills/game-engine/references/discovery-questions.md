---
name: discovery-questions
type: reference
parent: game-engine
---

# Discovery Questions — Per GDD Section

Questions the agent asks during Phase 1 Section Walkthrough (Step 3). Present one question at a time with options, tradeoffs, and recommendations.

## Initial Discovery (Step 1)

1. What kind of game do you want to make? (free-form, then narrow to genre)
2. What's the scope? (tiny/small/medium/large — explain each)
3. What platform/stack? (Python/Pygame, Godot, Phaser, LOVE — with tradeoffs)
4. What art style? (ASCII, pixel, simple shapes, etc.)

## Section 1: Game Loop
- What's the core cycle? (turn-based, real-time, hybrid)
- What does one "turn" or "frame" look like? (phases, order of operations)
- How long should a typical game session last?

## Section 2: World/Space
- What's the play space? (2D grid, hex, continuous, side-scroll, isometric)
- Is the world generated or hand-designed?
- How big is the world? (screen-sized, scrollable, infinite)
- Is there fog of war or hidden information?

## Section 3: Entities
- What are the main entity types? (player, enemies, items, buildings, etc.)
- What stats/properties do entities have?
- How are entities created and destroyed?
- Are there entity subtypes? (unit classes, enemy varieties)

## Section 4: Player Actions
- What can the player do each turn/frame?
- Are there action points or cooldowns?
- Which actions are reversible?

## Section 5: Rules/Mechanics
- What governs entity interactions? (combat, trading, matching)
- What's the damage/scoring formula?
- What modifiers exist? (terrain, buffs, equipment)
- What happens at boundaries? (0 HP, full inventory, edge of map)

## Section 6: Progression
- How does the player advance? (levels, tech tree, unlocks, story)
- What gates progress? (XP, resources, bosses, puzzles)
- Is progression permanent or per-session?

## Section 7: Win/Lose Conditions
- How does the player win? (score, objectives, survival, completion)
- How does the player lose? (death, time, resources, failure)
- Are there multiple victory types?
- Is there a draw condition?

## Section 8: UI/Rendering
- What information does the player need to see? (stats, map, inventory)
- What input methods? (keyboard, mouse, touch, gamepad)
- What's the layout? (panels, HUD, menus)

## Section 9: AI/Opponents
- What does the AI control? (enemies, NPCs, neutral parties)
- How smart should the AI be? (scripted, utility, learning)
- Do opponents have personalities or difficulty levels?

## Section 10: Economy/Resources
- What resources exist? (gold, mana, materials, time)
- How are resources gained and spent?
- Is there trading or exchange?
- What's the resource cap?

## Section 11: Randomness/Procedural
- What varies between playthroughs? (maps, encounters, loot)
- What's the randomness source? (seeded, pure random, weighted)
- Are there random events?

## Section 12: Multiplayer
- Is this single-player, co-op, or PvP?
- Real-time or turn-based multiplayer?
- Local or networked?

## Section 13: Narrative
- Is there a story? (campaign, emergent, environmental)
- How is story delivered? (dialogue, events, lore items)
- Does player choice affect narrative?

## Section 14: Audio/Visual Style
- What's the visual style? (ASCII, pixel, low-poly, stylized)
- What mood/atmosphere? (dark, cheerful, retro, epic)
- Is music important? (background, dynamic, none for v1)

## Section 15: Technical Architecture
- What major systems exist? (rendering, input, game logic, AI, audio)
- What patterns? (ECS, scene graph, state machine, event-driven)
- How do systems communicate? (events, direct calls, message bus)

## Section 16: Data Model
- What data is persistent? (saves, high scores, settings)
- What format? (JSON, SQLite, custom binary)
- Does the game need save/load?

## Section 17: Configuration
- What's user-configurable? (difficulty, controls, display)
- What's developer-configurable? (debug mode, spawn rates)

## Section 18: Balance Levers
- What values need tuning? (damage, costs, rates, thresholds)
- What's the difficulty model? (presets, scaling, adaptive)

## Section 19: Scope/Phases
- What's the MVP? (minimum playable version)
- What gets added in phase 2, 3, etc.?
- What's explicitly out of scope?

## Section 20: External Dependencies
- What data is sourced externally? (player stats, map data, card databases)
- What libraries are needed? (physics, noise, rendering)
- What assets are sourced? (sprites, sounds, fonts)
