---
name: game-play
type: command
domain: game-engine
kernel_loop: true
---

# /game-play

Execute a complete game session. Dispatch to appropriate loop system based on campaign state.

## Kernel Loop Integration

```
/kernel/anchor -> this command -> /kernel/complete
```

## Usage

```
/game-play [campaign-id] [auto-play-iterations=1]
```

Arguments:
- `campaign-id`: Campaign identifier (e.g., `campaign-2026-05-27-001`)
- `auto-play-iterations`: Number of game iterations to execute (default `1`)

## Instructions

1. **Party Check:**
   - Before loading campaign state, check `campaign.party` field
   - If `campaign.party` is null or empty:
     - Dispatch to character-creation-loop first
     - Wait for party creation to complete
     - Reload campaign state (now has party)
     - Proceed to step 2
   - If party exists:
     - Proceed to step 2 (normal game loop)

2. **Load campaign state:**
   - Read campaign via game-session skill contracts:
     - `projects/ai-dnd-game/.claude/skills/game-session/contracts/load-campaign-contract.json`
   - If no campaign-id provided, check for most recent campaign in `projects/ai-dnd-game/campaigns/`
   - If no campaign exists, report error: "No campaign found. Run /game-create then /game-build first."

3. **Evaluate state against decision rules:**
   - Read `projects/ai-dnd-game/contracts/state-evaluation-contract.json`
   - Apply decision rules in priority order (first match wins):

   | Priority | Condition | Output |
   |----------|-----------|--------|
   | 0 | `campaign.party == null OR campaign.party.length == 0` | character-creation-loop |
   | 1 | `status == 'wipe' OR status == 'complete'` | game-over |
   | 2 | `combat.active == true` | combat-loop |
   | 3 | `social.active == true` | social-loop |
   | 4 | `challenge.active == true` | challenge-loop |
   | 5 | `rest.active == true` | rest-loop |
   | 6 | `travel.active == true` | travel-loop |
   | 99 | `else` | narration-skill |

4. **Dispatch to loop system:**
   - Invoke the matched loop system via its skill:
     - `character-creation-loop` → character-creation-loop skill (`.claude/skills/game-engine/character-creation-loop.md`)
     - `combat-loop` → combat skill
     - `social-loop` → scene skill (social mode)
     - `challenge-loop` → challenge skill
     - `rest-loop` → rest skill
     - `travel-loop` → scene skill (travel mode)
     - `narration-skill` → narration skill
     - `game-over` → report final state and stop

5. **Execute loop iteration:**
   - The loop skill handles one complete iteration (turn, encounter, scene)
   - Loop skill reads/writes campaign state via game-session contracts
   - Loop skill applies atomic operations via atomic-ops skill contracts

6. **Save campaign state:**
   - Persist state via game-session save contract:
     - `projects/ai-dnd-game/.claude/skills/game-session/contracts/save-session-contract.json`
   - Log the iteration result to session transcript

7. **Repeat or complete:**
   - Decrement remaining iterations
   - If iterations remain AND no game-over condition: return to step 3
   - If game-over or iterations exhausted: proceed to completion

## Inputs

- Campaign state (loaded via game-session contract)
- State evaluation rules (from `state-evaluation-contract.json`)

## Outputs

- Executed campaign with state persisted after each iteration
- Session transcript with action log per iteration
- State evaluation decision applied and logged

## Key Contracts

| Contract | Location | Purpose |
|----------|----------|---------|
| State Evaluation | `projects/ai-dnd-game/contracts/state-evaluation-contract.json` | Map campaign state to loop system |
| Load Campaign | `projects/ai-dnd-game/.claude/skills/game-session/contracts/load-campaign-contract.json` | Load campaign state |
| Save Session | `projects/ai-dnd-game/.claude/skills/game-session/contracts/save-session-contract.json` | Persist state after iteration |

## Constraints

- Fully contract-driven — no Python implementation
- Delegates to loop systems (skills) for all game logic
- Reads/writes campaign state exclusively via game-session contracts
- Decision routing uses state-evaluation-contract.json — never hardcoded

## On Failure

- Read `steps/on-failure.md` for diagnosis
- Fix → `/kernel/learn` → retry (max 3)

## On Completion

- Report: "Session complete — N iterations executed, final state: [state summary]."
- `/kernel/complete`
