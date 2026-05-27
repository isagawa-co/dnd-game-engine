# Game Orchestration: Contract-Driven Redesign

## Status
Open

## Priority
High — Game-play command expects contract-driven loops; current implementations violate prescriptive architecture (commands → skills → contracts only)

## Summary

The game orchestration layer (scene dispatcher, campaign loop, character-creation loop) must be fully contract-driven per the prescriptive game-engine protocol. Currently: (1) **scene dispatcher** has Python stubs instead of contracts; (2) **campaign loop** has Python code (campaign-loop.py, arc-transition.py, state-manager.py) instead of contracts; (3) **character-creation-loop** skill and contracts are missing entirely. All three must be redesigned to pure contract-driven architecture: SKILL.md + contracts only, no Python orchestration code. Integration point: `/game-play` command dispatches to these loops based on state-evaluation-contract.json rules.

## Design Documents

| Document | Purpose |
|----------|---------|
| [[023-game-refactor-orchestration-contract-driven/scene-dispatcher]] | Scene dispatcher contract-driven redesign (5 contracts: action, outcome, dispatch, encounter-types, workflow) |
| [[023-game-refactor-orchestration-contract-driven/campaign-loop]] | Campaign loop refactor (remove campaign-loop.py/arc-transition.py/state-manager.py; add contracts for arc progression, state mutations) |
| [[023-game-refactor-orchestration-contract-driven/character-creation-loop]] | New character-creation-loop skill (SKILL.md + 3 contracts: creation-action, creation-outcome, validation) |
| [[023-game-refactor-orchestration-contract-driven/integration-flow]] | How /game-play orchestrates all three loops via state-evaluation-contract.json routing |

## Architecture Flow

```
/game-play [campaign-id]
  ↓ reads state-evaluation-contract.json
  ↓ evaluates campaign.party, combat.active, social.active, etc.
  ├─→ if party missing: invoke character-creation-loop
  ├─→ if combat active: invoke combat-loop (already built)
  ├─→ if scene active: invoke scene-loop (dispatcher)
  │     ├─→ scene dispatcher reads encounter_type
  │     └─→ dispatches to appropriate sub-loop (combat, challenge, rest, etc.)
  ├─→ if campaign arc active: invoke campaign-loop
  │     ├─→ evaluates arc completion rules
  │     └─→ returns arc outcome (victory, defeat, next-arc)
  └─→ persists all outcomes to campaign state

All interactions validated against contracts before execution
```

## Requirements

- **Scene dispatcher** must be contract-driven (no Python dispatch code)
- **Campaign loop** must remove all Python implementation (campaign-loop.py, arc-transition.py, state-manager.py)
- **Character-creation-loop** must be fully defined with SKILL.md + contracts
- All three loops must validate inputs/outputs against contracts
- Integration via `/game-play` must route based on state-evaluation-contract.json (not hardcoded logic)
- No Python orchestration code in loop layer (implementation code for specific operations OK, but not routing/dispatching)

## References

- `/game-play` command: `.claude/commands/game-play.md`
- State evaluation: `projects/ai-dnd-game/contracts/state-evaluation-contract.json`
- Existing contracts: atomic-ops, challenge, configuration, rest (1 contract)
- Game engine protocol: `.claude/protocols/game-engine-protocol.md`

## Task Builder Input

- **Deliverable:**
  - Scene dispatcher: SKILL.md + 5 contracts (action, outcome, dispatch, encounter-types, workflow)
  - Campaign loop: SKILL.md + 4 contracts (arc-progression, state-mutation, phase-transition, completion-rules)
  - Character-creation loop: SKILL.md + 3 contracts (action, outcome, validation)
  - Integration: Updated /game-play command documentation + contract references

- **Location:** `new-repo:D:\my_ai_projects\project_test_repos\dnd-game-engine-test` (update existing skills in golden master)

- **Scope:** REFACTOR (convert existing implementations to contract-driven) + BUILD (new character-creation-loop)

- **Constraints:**
  - Must maintain compatibility with existing sub-loops (combat, challenge, rest, etc.)
  - All contracts must follow atomic-ops/challenge/configuration patterns
  - No Python code in orchestration layer (only SKILL.md + contracts)
  - Integration point: `/game-play` must dispatch via contract evaluation, not hardcoded logic
  - Output goes to golden master repo (dnd-game-engine-test)
