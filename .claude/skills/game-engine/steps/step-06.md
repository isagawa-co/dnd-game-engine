---
step: 6
name: Decompose GDD
requires: approved_gdd, gate_pass
produces: ordered_backlog_items
---

# Step 6: Decompose GDD into Backlog Items

## Purpose

Automatically convert the completed GDD into ordered backlog items, one per game system. Identify dependencies between systems and order the backlog so each item can be built with its dependencies already in place. This step is fully automatic — no HITL.

## Input

- All `docs/game-design/sections/*.md` — completed GDD sections
- `docs/game-design/profile.md` — genre, platform, scope

## Actions

1. **Read all GDD sections** — identify discrete game systems
2. **Map systems** — each major system becomes one backlog item:
   - Core systems (must build first): game loop, world/map, entities
   - Dependent systems (need core): combat, economy, AI, progression
   - Infrastructure (parallel): UI/rendering, data model, configuration
   - Integration (last): balance, external deps, scope/phases
3. **Build dependency graph:**
   ```
   game-loop (no deps)
     → world-map (needs game-loop)
       → entities (needs world-map)
         → combat (needs entities)
         → economy (needs entities)
           → ai-opponents (needs combat + economy)
     → ui-rendering (needs game-loop)
   configuration (no deps, parallel)
   data-model (no deps, parallel)
   ```
4. **Generate backlog items** — one `.md` file per system:
   ```markdown
   # [System Name] System

   ## GDD Section
   Section NN: [name]

   ## Dependencies
   - [list systems that must be built first]

   ## REQ IDs
   - REQ-SYS-001: [behavior]
   - REQ-SYS-002: [behavior]
   [pulled directly from GDD section]

   ## Acceptance Criteria
   - All REQ IDs have passing tests
   - Tests include REQ ID in function name
   - No hardcoded balance values (config only)
   ```
5. **Write backlog** — save to `backlog/NNN-system-name.md` in dependency order
6. **Generate backlog index** — `backlog/000-index.md` with system list and dependency graph

## Output

- `backlog/NNN-system-name.md` — one per system, ordered by dependencies
- `backlog/000-index.md` — index with dependency graph
- State updated with systems list

## Verification

- [ ] Every GDD section maps to at least one backlog item
- [ ] Dependency ordering is acyclic (no circular deps)
- [ ] Each backlog item lists its REQ IDs from the GDD
- [ ] Backlog items are numbered in dependency order
- [ ] Index file shows complete dependency graph

## Failure Modes

| Failure | Symptom | Recovery |
|---------|---------|----------|
| Circular dependency | System A needs B, B needs A | Identify shared core, extract as separate system |
| Too many items | 20+ backlog items for medium scope | Merge related systems (e.g., combat + unit management) |
| Missing REQ IDs | Backlog item has no REQs | Re-read GDD section, every testable behavior needs a REQ |
| Scope creep | Decomposition reveals systems not in GDD | Only decompose what's in the GDD, flag gaps for user |

## Example

**4X Strategy Game → Decomposition:**

```
001-game-loop.md          ← Core loop (explore/expand/exploit/exterminate phases)
002-world-map.md          ← Terrain, hex grid, fog of war, map generation
003-entities.md           ← Civilizations, units, buildings, stat tables
004-player-actions.md     ← Movement, founding, building, diplomacy actions
005-combat.md             ← Damage formula, modifiers, siege, ZoC
006-economy.md            ← Gold, science, faith, happiness, trade
007-progression.md        ← Tech tree, eras, policies, religion
008-ai-opponents.md       ← Personality weights, utility scoring, barbarians
009-ui-rendering.md       ← ASCII layers, panels, input handling
010-data-model.md         ← Civ/unit/building data structures
011-configuration.md      ← Map size, difficulty, game speed settings
012-balance.md            ← Yield multipliers, cost curves, spawn rates
013-external-deps.md      ← Simplex noise, terminal rendering libs
```
