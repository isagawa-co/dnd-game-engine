# Scene Loop — Skill Definition

## Loop Execution Protocol (MANDATORY)

The scene loop is the WITHIN-SCENE router. Run it per the canonical protocol — strict outer→inner layering, re-read each step, never from memory: → [[../campaign/references/loop-execution-protocol.md]]

- **Layering:** finish read → identify `encounter_type` → validate BEFORE dispatching a sub-loop. Only dispatch a sub-loop whose skill directory exists (no stub/missing handler).
- **On dispatch:** set the sub-loop's flag + `active_loop.loop` per that sub-loop's entry rule; wait for its Return Outcome before processing.
- **On sub-loop return:** apply state mutations (step 6), then re-evaluate for the next encounter or return up to campaign.
- **Render:** call the render skill (`.claude/skills/render/SKILL.md`) on entering a location to draw the scene map above the menu.
- **Output format:** `.claude/skills/action-prompt/SKILL.md`.

## Identity

| Key | Value |
|-----|-------|
| Skill | scene |
| Type | sub-loop |
| Parent | campaign-loop |
| Purpose | Dispatch encounters to sub-loops (combat, social, challenge, merchant, rest, travel, item-use) and process outcomes |

## Vocabulary

| Term | Definition |
|------|-----------|
| Scene | A location with NPCs, environment, and encounter definitions |
| Encounter | A discrete interaction within a scene (combat, social, challenge, etc.) |
| Dispatcher | Routes encounter data to the appropriate sub-loop based on type |
| Outcome | Result returned by a sub-loop (victory, success, failure, etc.) |
| State Mutation | Atomic update to entity state (HP, inventory, conditions) after outcome |

## Contracts

| Contract | File |
|----------|------|
| Input | → [[contracts/scene-action-contract.json]] |
| Output | → [[contracts/scene-outcome-contract.json]] |
| Dispatch | → [[contracts/scene-dispatch-contract.json]] |
| Encounter Types | → [[contracts/scene-encounter-types.json]] |

## Resolution Flow

1. Campaign loop sends scene data (location, NPCs, encounter definitions)
2. Scene dispatcher identifies encounter type from `encounter_type` field
3. `validate_encounter()` validates input against action contract per type
4. `dispatch_encounter()` routes to appropriate sub-loop handler
5. Sub-loop resolves encounter and returns outcome dict
6. `process_outcome()` applies state mutations and returns updated state to campaign loop

## 7 Encounter Types

| Type | Sub-Loop | Skill | Status |
|------|----------|-------|--------|
| combat | combat-loop | → [[.claude/skills/combat/SKILL.md]] | built |
| social | social-loop | → [[.claude/skills/social/SKILL.md]] | built |
| challenge | challenge-loop | → [[.claude/skills/challenge/SKILL.md]] | built |
| merchant | merchant-loop | → [[.claude/skills/merchant/SKILL.md]] | built |
| rest | rest-loop | → [[.claude/skills/rest/SKILL.md]] | built |
| travel | travel-loop | → [[.claude/skills/travel/SKILL.md]] | built |
| item-use | item-use-loop | → [[.claude/skills/item-use/SKILL.md]] | built |

## Action Prompt Integration

At every decision point within a scene, use the **action-prompt** skill (`.claude/skills/action-prompt/SKILL.md`) for standardized presentation. The scene loop determines the context (`exploration`, `social`, `combat_turn`, etc.) and the action-prompt skill handles numbered options + custom input.

## Integration

- **Depends on:** atomic_ops (ability checks, damage), entity (PC/NPC/monster state), action-prompt (user choice presentation)
- **Returns to:** campaign-loop (outcome dict triggers state mutations + narration)
- **Design doc:** → [[backlog/007-dnd-build-scene-loop/encounter-types.md]]

## Tests

→ [[tests/]]
