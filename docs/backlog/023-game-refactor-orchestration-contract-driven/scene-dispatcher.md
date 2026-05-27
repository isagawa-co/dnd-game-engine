# Scene Dispatcher — Contract-Driven Redesign

## Status
NEW

## Location
`.claude/skills/scene/` (refactor existing SKILL.md + add 5 contracts)

## What

Convert the scene dispatcher from Python stub handlers to pure contract-driven routing. Scene dispatcher routes encounters (combat, social, challenge, merchant, rest, travel, item-use) to appropriate sub-loop skills based on encounter_type. Currently: scene_dispatcher.py has hardcoded stub implementations. Must convert to: SKILL.md (routing rules) + 5 contracts (action schema, outcome schema, dispatch table, encounter types, validation).

## Deliverables

1. **scene/SKILL.md** (updated) — remove references to Python dispatcher, add routing rules as contracts
2. **scene/contracts/scene-action-contract.json** — input from campaign: scene data + encounter definition
3. **scene/contracts/scene-outcome-contract.json** — output to campaign: encounter result
4. **scene/contracts/scene-dispatch-contract.json** — routing table mapping encounter_type → sub-loop skill paths
5. **scene/contracts/scene-encounter-types.json** — catalog of 7 encounter types with input/output schemas
6. **scene/workflow.md** — how orchestrator reads contracts and invokes sub-loops (reference file)

## Dependencies

- Depends on: campaign-loop (parent), combat/challenge/rest/etc (sub-loops)
- No Python code — contracts + reference docs only
- Orchestrator (campaign-loop) reads dispatch-contract to route encounters

## Integration Point

Game-play command → campaign-loop → scene-loop (for scene encounters)

Scene dispatcher validates:
- Incoming scene-action against scene-action-contract.json
- Encounter type exists in dispatch-contract.json
- Encounter.data matches scene-encounter-types.json[type].input_schema
- Sub-loop outcome matches output-contract
- Final outcome matches scene-outcome-contract.json
