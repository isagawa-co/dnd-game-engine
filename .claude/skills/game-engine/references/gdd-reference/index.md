# GDD Reference Implementation — Tiny Civ 4X

**Source:** "Making a Tiny Civ Game with Claude" blog series (Parts 1 & 2)
**Genre:** 4X Strategy
**Stack:** ASCII terminal rendering
**Scope:** 20 systems, 6 victory conditions, 6 eras, 16+ unit types

## Purpose

This is a fully worked GDD example showing what "done" looks like for each section. During Phase 1 discovery, the agent reads the corresponding section before walking the user through it — calibrating for the expected level of granularity (data tables, formulas, enumerations, edge cases).

The content is genre-specific (4X strategy) but the **structure and depth** are the universal standard.

## Sections

| # | Template Section | Reference File | Tiny Civ Content |
|---|-----------------|----------------|-----------------|
| 1 | Game Loop | [[01-game-loop]] | Explore → Expand → Exploit → Exterminate, turn structure |
| 2 | World/Space | [[02-world-space]] | Terrain grid, 10 tile types with yields, fog of war, map gen |
| 3 | Entities | [[03-entities]] | Civs, units (15 military + 4 civilian), buildings (16), wonders (8) |
| 4 | Player Actions | [[04-player-actions]] | Movement, founding, building, tile improvements |
| 5 | Rules/Mechanics | [[05-rules-mechanics]] | Combat formula, modifiers, city siege, zone of control |
| 6 | Progression | [[06-progression]] | Tech tree (6 eras), civic policies (6 trees), governments (7), religion |
| 7 | Win/Lose | [[07-win-lose]] | 6 victory conditions with exact triggers |
| 8 | UI/Rendering | [[08-ui-rendering]] | ASCII layers, 8 panels, keyboard input mapping |
| 9 | AI/Opponents | [[09-ai-opponents]] | Personality weights (7 dimensions), utility scoring, 5 presets, barbarians |
| 10 | Economy/Resources | [[10-economy]] | Gold/science/faith/culture/happiness, trade routes, great people |
| 11 | Randomness/Procedural | [[11-randomness]] | Simplex noise map gen, 5 random events, resource placement |
| 12 | Narrative/Lore | [[12-narrative]] | History log, era progression, event announcements |
| 13 | Audio/Visual Style | [[13-audio-visual]] | Hand-drawn ASCII, era-themed styling |
| 14 | Technical Architecture | [[14-architecture]] | 16 core systems, data-driven design |
| 15 | Data Model | [[15-data-model]] | Data files for civs, techs, units, buildings, beliefs, events |
| 16 | Configuration | [[16-configuration]] | Map size, civ count, difficulty, game speed, victory toggles |
| 17 | Balance Levers | [[17-balance]] | 9 tuning knobs with descriptions |
| 18 | Scope/Phases | [[18-scope-phases]] | 4 phases: core → depth → systems → polish |
| 19 | External Dependencies | [[19-external-deps]] | Simplex noise, terminal rendering |

## Requirements Traceability (from Part 2)

The blog author also documented a requirements-driven approach:
- Requirements stored in `/docs/requirements/` as markdown, one file per system
- REQ IDs follow `REQ X-NNNN` format (e.g., REQ 1-0101)
- Test names include REQ IDs: `it('should... [REQ-1-0101]')`
- Coverage script cross-references REQs → test names → pass/fail report
- See [[requirements-approach]] for the full methodology
