# D&D Game Engine — Golden Master

This is the definitive D&D 5e game engine implementation. Fully contract-driven, agent-orchestrated, and ready for production use.

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
- `.claude/skills/challenge/SKILL.md` — Challenge resolution
- `.claude/skills/rest/SKILL.md` — Rest mechanics
- `.claude/skills/character/SKILL.md` — Character creation
- `.claude/skills/game-engine/` — Domain specification

### Contracts
- `projects/ai-dnd-game/contracts/` — State evaluation, campaign loop, character creation
- `.claude/skills/*/contracts/` — Skill-specific input/output schemas

### Campaigns
- `projects/ai-dnd-game/campaigns/` — Saved campaign state
- `projects/ai-dnd-game/content/` — Content packs (monsters, items, spells, NPCs)

## Testing

1. **Create a campaign** via `/game-create` and `/game-build`
2. **Play it** via `/game-play [campaign-id]`
3. **Provide rolls** when agent prompts
4. **Verify** state updates correctly after each iteration
5. **Test multi-session** by invoking `/game-play [campaign-id]` again

## Critical Reminders for Agents

- **You are the DM.** Read skills, understand rules, make game decisions.
- **User provides rolls.** Prompt "Roll d20" → user says "I got 17" → you use that.
- **Update JSON state.** After each iteration, campaign_state.json reflects results.
- **No Python execution.** You don't run code. You read contracts and apply them.
- **Fully interactive.** This is collaborative: agent narrates, user rolls.
- **Check for relevant commands/skills on every action.** Before taking any game action (character creation, combat, challenge resolution, rest, etc.), verify if a matching command or skill exists. Read and follow that skill's instructions exactly. Never improvise game logic—always read the prescriptive skill first.

---

Ready to play. Invoke `/game-play [campaign-id]` to begin.
