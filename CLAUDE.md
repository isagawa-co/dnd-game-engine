# D&D Game Engine — Golden Master

This is the definitive D&D 5e game engine implementation. Fully contract-driven, agent-orchestrated, and ready for production use.

## MANDATORY: Anchor Protocol

**NEVER shortcut the anchor.** When the action counter triggers an anchor (or you invoke `/kernel/anchor`), you MUST execute the FULL protocol — every step, every read, every review. This means:

1. **Read** `.claude/protocols/game-engine-protocol.md` — use the Read tool, not memory
2. **Read** `.claude/lessons/lessons.md` — use the Read tool, not memory
3. **Apply rules** to your specific next action with concrete verbs ("I will X before Y")
4. **Read** `.claude/state/session_state.json` to restore context
5. **Read** `.claude/state/actions.jsonl` and review every action against protocol
6. **Archive** the actions log, reset counters, confirm the anchor token
7. **Use the Skill tool** to invoke `/kernel/anchor` — do not manually flip state flags

Skipping ANY step is a violation. "Quick anchor" (just confirming the token) is a violation. Reading from memory instead of using the Read tool is a violation. The anchor exists to re-center on protocol, not to reset a counter.

## Game Architecture

### Core Principle: Agent-Orchestrated Interactive TTRPGs

This game is **FULLY ORCHESTRATED BY THE AGENT**, not code-driven:

1. **Agent is the Dungeon Master (DM)**
   - Reads prescriptive skills (Markdown instructions)
   - Describes situations, generates encounters, applies rules
   - Prompts the user to roll dice
   - Uses user-provided rolls to resolve outcomes
   - Updates campaign state (JSON files)

2. **User is the Player**
   - Rolls dice (provides actual numbers to agent)
   - Makes decisions (what character does)
   - Narrates actions
   - Agent responds with consequences

3. **No Python Game Code**
   - Python was only for testing infrastructure
   - Gameplay is 100% driven by agent reading contracts and skills
   - All state lives in JSON

### Interactive Game Loop

Standard flow for each iteration:

```
Agent: "You're on the forest road. Ahead, 3 goblins block your path!"
       "Roll initiative. d20 + your DEX modifier."

User: "I got 14 total"

Agent: "Goblins rolled 9. You act first. What do you do?"

User: "I attack with my longsword"

Agent: "Roll your attack roll (d20 + 5 to hit, DC 10)"

User: "I rolled 18"

Agent: "Hit! Roll damage (d8 + 3)"

User: "I rolled 6"

Agent: "Your sword strikes for 6 damage. The first goblin falls.
        Two remain. Goblin 1 attacks you..."

[Continue until encounter ends]

Agent: "You win. Collect 15 gold and a dagger.
        Session 18 complete. Returning to town."

[State saved]
```

## Commands

### `/game-create`
**Phase 1:** Create a new Game Design Document (GDD) through guided discovery
- Genre selection, scope, mechanics
- Complete GDD for building

### `/game-build`
**Phase 2+3:** Decompose GDD into game systems, build all infrastructure
- Creates campaigns, content packs, contracts, skills
- Autonomous task execution

### `/game-play [campaign-id]`
**Phase 4 (Production):** Play a campaign interactively
- Load saved campaign
- Agent describes situation
- Agent prompts for rolls
- User provides roll numbers
- Agent resolves outcomes
- Repeat until session/game end

## Skills (Prescriptive Instructions for Agent)

Agent reads these to understand how to run the game:

| Skill | Purpose | How It Works |
|-------|---------|-------------|
| Campaign Loop | Orchestrate 5-step game cycle | Agent follows 5 steps, prompting user for rolls at each decision point |
| Scene Loop | Dispatch to encounter types | Agent uses current campaign state to decide what type of scene (combat, social, exploration, etc.) |
| Challenge Loop | Resolve skill checks | Agent prompts "Make a Strength check (DC 12)", user rolls, agent applies result |
| Combat Loop | Handle combat rounds | Agent describes attacks, prompts for rolls, tracks initiative, applies damage |
| Rest Loop | Handle long/short rest | Agent applies healing, spell slot recovery, uses rules |
| Character Skill | Create/level characters | Agent prompts for ability score rolls (4d6 drop lowest), class selection, equipment |
| Scene Skill | General scene resolution | Agent uses encounter tables to generate random encounters |

## Contracts (JSON Rules)

Machine-readable specifications that agent follows:

| Contract | Purpose | Agent Uses It For |
|----------|---------|-------------------|
| state-evaluation | Decision rules | Decide which loop to run based on campaign state |
| challenge-action | Challenge input schema | Validate user's action ("Make Athletics check") |
| challenge-outcome | Challenge output schema | Record result ("success" / "failure" + consequence) |
| character-creation | Character building | Create 5-tier entities with ability scores, class, HP, etc. |
| campaign-loop | Campaign state machine | Manage 5-tier state (campaign → arc → session → scene → combat) |

## To Play a Game

### Step 1: Create a Campaign
```
/game-create
[Answer discovery questions to build GDD]
/game-build
[Autonomous system build—creates campaigns, content, contracts]
```

### Step 2: Play It
```
/game-play [campaign-id]
```

Agent will:
1. Load the campaign
2. Describe the current situation
3. Prompt: "Roll d20 for initiative" (or other action)
4. You provide the number you rolled
5. Agent resolves using that number
6. Repeat until iteration complete
7. State saved automatically

### Example Session
```
Agent: "You awaken in the Sword Coast Inn. Morning sun streams through
        the tavern windows. A hooded figure in the corner catches your eye."

Agent: "Do you approach the figure, talk to the bartender, or do something else?"

You: "I approach the figure and try to get information from them"

Agent: "Make an Insight check to read their intent (DC 12)"

You: "I rolled 14"

Agent: "You sense they're nervous but not hostile. They slide a piece of parchment
        across the table. 'I need adventurers,' they whisper..."

[Encounter continues until resolved]
```

## Architecture Layers

```
Agent (DM)
  ↓ reads
Prescriptive Skills (Markdown: Campaign, Scene, Challenge, etc.)
  ↓ applies
Contracts (JSON: decision rules, state schemas, mechanics)
  ↓ updates
Campaign State (JSON: persists across sessions)
  ↓
User sees narration + is prompted for rolls
  ↓ provides
Roll Numbers (user input)
```

## Key Files

### Commands
- `.claude/commands/game-create.md` — Create GDD
- `.claude/commands/game-build.md` — Build from GDD
- `.claude/commands/game-play.md` — Play campaign interactively

### Skills
- `.claude/skills/campaign/SKILL.md` — Campaign loop (5 steps)
- `.claude/skills/scene/SKILL.md` — Scene dispatch
- `.claude/skills/combat/SKILL.md` — Combat loop (initiative, rounds, actions, outcomes)
- `.claude/skills/challenge/SKILL.md` — Challenge resolution
- `.claude/skills/rest/SKILL.md` — Rest mechanics
- `.claude/skills/character/SKILL.md` — Character creation
- `.claude/skills/action-prompt/SKILL.md` — Standardized action menu presentation
- `.claude/skills/state-check/SKILL.md` — Post-action state validation (soft enforcement)
- `.claude/skills/game-engine/` — Domain specification

### Hooks (Hard Enforcement)
- `.claude/hooks/universal-gate-enforcer.py` — Anchor, session, learn gates
- `.claude/hooks/game-state-enforcer.py` — Game state persistence enforcement

### Contracts
- `contracts/` — State evaluation, campaign loop, character creation
- `.claude/skills/*/contracts/` — Skill-specific input/output schemas

### Campaigns
- `campaigns/` — Saved campaign state
- `adventures/` — Adventure packs (scenes, monsters, items, spells, NPCs)

## Testing

1. **Create a campaign** via `/game-create` and `/game-build`
2. **Play it** via `/game-play [campaign-id]`
3. **Provide rolls** when agent prompts
4. **Verify** state updates correctly after each iteration
5. **Test multi-session** by invoking `/game-play [campaign-id]` again

## MANDATORY: State Check After Every Action (Defense in Depth)

**After every resolved game action, you MUST run the state-check before narrating results.**

Two layers enforce this — both are mandatory:

### Layer 1 — Soft (state-check skill)
Read `.claude/skills/state-check/SKILL.md`. After every resolved action (combat round, skill check, loot pickup, quest update, rest, travel), run the 10-item checklist:

1. HP changed? → update state
2. Resources spent? → update spell slots, ammo, class features
3. Loot gained? → add to loot_collected
4. XP earned? → update party_xp
5. Quest updated? → update quests array
6. Location changed? → update current_location
7. NPCs encountered? → update npcs array
8. Conditions changed? → update character conditions
9. Combat state changed? → update combat object
10. Act/chapter progressed? → update current_act, current_act_id

Output the STATE CHECK block, save campaign_state.json, THEN narrate.

### Layer 2 — Hard (game-state-enforcer.py hook)
The hook blocks you if you skip the state check:

- **Scene transition gate:** Cannot read next act file without saving state first
- **Combat end validation:** Cannot set combat.active=false without XP, loot, and last_combat fields
- **Act transition validation:** Cannot change current_act_id without session_notes
- **Periodic save:** Blocked after 5 game-file writes without saving campaign_state.json

You cannot bypass these. If the hook blocks you, run the state-check skill and save state.

## Critical Reminders for Agents

- **You are the DM.** Read skills, understand rules, make game decisions.
- **User provides rolls.** Prompt "Roll d20" → user says "I got 17" → you use that.
- **Update JSON state.** After each iteration, campaign_state.json reflects results.
- **No Python execution.** You don't run code. You read contracts and apply them.
- **Fully interactive.** This is collaborative: agent narrates, user rolls.
- **State check is not optional.** Run the checklist after every action. The hook enforces this.
- **Check for relevant commands/skills on every action.** Before taking any game action (character creation, combat, challenge resolution, rest, etc.), verify if a matching command or skill exists. Read and follow that skill's instructions exactly. Never improvise game logic—always read the prescriptive skill first.

---

Ready to play. Invoke `/game-play [campaign-id]` to begin.
