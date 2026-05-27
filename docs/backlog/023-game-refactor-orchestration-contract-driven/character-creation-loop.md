# Character Creation Loop — New Skill Definition

## Status
NEW — does not exist yet

## Location
`.claude/skills/character-creation-loop/` (create new skill with SKILL.md + 3 contracts)

## What

Character creation loop is referenced by /game-play command but does not exist. Manages party creation: orchestrate PC creation workflow, validate race/class registry lookups, enforce party composition rules (casters vs martial, level balance), integrate with extended-character-system registries (all-races.json, all-classes.json), return party state to campaign.

## Requirements

- **Input:** campaign_id, party_size (3-6 PCs), starting_level (1-20)
- **Output:** party state with 3-6 PC objects (each with race, class, abilities, proficiencies, etc.)
- **Registry lookups:** all-races.json, all-classes.json from content system
- **Validation:** party composition (must have at least 1 caster, 1 martial), level consistency, race/class existence in registries
- **Integration:** extended-character-system (backlog 022) provides registries + PC creation logic

## Deliverables

1. **character-creation-loop/SKILL.md** — identity, vocabulary, architecture, contracts
2. **character-creation-loop/contracts/character-creation-action-contract.json** — input: campaign_id, party_size, starting_level
3. **character-creation-loop/contracts/character-creation-outcome-contract.json** — output: party state with 3-6 validated PCs
4. **character-creation-loop/contracts/party-validation-contract.json** — rules: party composition, level bounds, race/class registry validation
5. **character-creation-loop/workflow.md** (reference) — how character creation loop validates and creates party

## Dependencies

- Depends on: extended-character-system (backlog 022) for PC creation contract + registries
- Used by: /game-play command (before gameplay, if party is null)

## Integration Point

/game-play command:
1. Check if campaign.party is null
2. If yes → invoke character-creation-loop
3. Receive party state (validated)
4. Assign to campaign
5. Continue with gameplay

## Key Contracts

All input/output must match character-creation-action-contract and character-creation-outcome-contract. Party validation per party-validation-contract before returning to game-play.
