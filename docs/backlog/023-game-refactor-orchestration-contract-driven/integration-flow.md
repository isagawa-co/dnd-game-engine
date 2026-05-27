# Game Orchestration Integration Flow

## Status
NEW — design document for how /game-play orchestrates all three redesigned loops

## Location
REFERENCE ONLY — describes orchestrator pattern used by `/game-play` command and `game-session` skill

## High-Level Architecture

```
/game-play [campaign-id] [iterations]
  ↓ (main orchestrator — reads contracts, makes routing decisions)
  ├─ Load campaign state via state-evaluation-contract.json
  │    ├─ campaign.party exists?
  │    │    No → DISPATCH: character-creation-loop
  │    │    Yes → continue
  │    ├─ campaign.status == 'wipe' or 'complete'?
  │    │    Yes → DISPATCH: game-over
  │    │    No → continue
  │    ├─ combat.active == true?
  │    │    Yes → DISPATCH: combat-loop
  │    │    No → continue
  │    ├─ scene.active == true?
  │    │    Yes → DISPATCH: scene-loop (dispatcher routes to sub-loops)
  │    │    No → continue
  │    └─ (default) → DISPATCH: narration-skill
  │
  ├─ Invoke appropriate loop via contract
  │    ├─ character-creation-loop: validate input vs character-creation-action-contract
  │    │    └─ return party state (character-creation-outcome-contract)
  │    ├─ combat-loop: validate input vs combat-loop-contract
  │    │    └─ return combat outcome (combat-loop-contract outcome schema)
  │    ├─ scene-loop: validate input vs scene-action-contract
  │    │    ├─ dispatcher reads encounter_type
  │    │    ├─ routes to sub-loop (combat, challenge, rest, merchant, social, travel, item-use)
  │    │    └─ return scene outcome (scene-outcome-contract)
  │    ├─ campaign-loop: validate input vs campaign-action-contract
  │    │    ├─ evaluates arc completion per arc-progression-contract
  │    │    └─ return arc outcome (campaign-outcome-contract)
  │    └─ narration-skill: validate input vs narration-request-contract
  │         └─ return narrative text (narration-output-contract)
  │
  ├─ Apply state mutations (per outcome contract)
  │    ├─ Update party state (HP, conditions, inventory)
  │    ├─ Update campaign state (time, XP, loot, plot flags)
  │    ├─ Update arc state (quests, NPCs, factions)
  │    └─ Persist to campaign.json via game-session save-session-contract
  │
  ├─ Persist state via game-session skill
  │    └─ Write campaign state atomically (save-session-contract)
  │
  └─ Loop N times (iterations parameter)
       Decrement iterations
       If iterations > 0 → return to Load campaign state step
       Else → /kernel/complete
```

## Contract Validation Flow

**Before invoking any loop:**
1. Validate orchestrator input against state-evaluation-contract.json
2. Validate loop input against [loop]-action-contract.json
3. Invoke loop (contracts define rules, no Python dispatch code)
4. Receive loop output
5. Validate output against [loop]-outcome-contract.json
6. Apply state mutations per [loop]-mutation-contract.json
7. Persist state atomically

**All contracts must:**
- Follow atomic-ops/challenge/configuration pattern
- Define input schema clearly
- Define output schema clearly
- Define validation rules (no Python code — contracts are data)

## Three Loop Redesigns Enable Clean Orchestration

1. **Scene Dispatcher** → routes encounters to sub-loops via contract dispatch table
2. **Campaign Loop** → defines arc progression rules via contract, not Python code
3. **Character Creation Loop** → validates party creation via contract, not embedded logic

**Result:** /game-play is pure orchestrator that reads contracts and invokes loops. No hardcoded routing, no Python dispatch logic. Everything is contract-driven.
