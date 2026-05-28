# Game Loop Integration

## Status
NEW

## Location
`workspace:.claude/commands/game-play.md`, `workspace:.claude/skills/campaign/SKILL.md`

## What It Does
Update the game-play command and campaign loop skill to:
1. Load the adventure manifest on startup
2. Check if current chapter's scene files exist — build them if missing
3. Read the current act file and follow it (not improvise)
4. Advance through acts via transitions
5. Track current_chapter and current_act in campaign state

## Game-Play Command Updates

Add between "Load campaign state" and "Evaluate state":

```
Step 2.5: Load Adventure
  - Read campaign.json → get adventure_id (e.g., "lmop")
  - Read adventures/[id]/manifest.json → verify adventure exists
  - Read campaign_state.json → get current_chapter and current_act
  - If current_chapter scenes don't exist → build them from training knowledge
  - Read current act file → this is the script for this iteration
```

## Campaign Loop Skill Updates

Update Step 3 (Play Campaign):
```
  - Read current act.json
  - Present read_aloud text to user
  - Present action menu using action-prompt skill with context from act data
  - Resolve encounters per act's encounter definitions
  - Use monster stat blocks from adventures/[id]/monsters/
  - Follow transitions to determine next act
  - CONSTRAINT: Do not narrate events, NPCs, or encounters not in the act file
```

## Campaign State Schema Additions

Add to campaign_state.json:
```json
{
  "adventure_id": "lmop",
  "current_chapter": 1,
  "current_act": "I",
  "current_act_id": "ch1-act-I",
  "chapters_completed": []
}
```

## Anti-Drift Rule

Add to campaign loop SKILL.md:
> **MANDATORY: The agent MUST read the current act file before narrating. All encounters, NPCs, locations, and plot beats come from the act file. The agent may add flavor text and dialog but MUST NOT invent new encounters, NPCs, or plot points not defined in the act. If the act file doesn't exist, build it before proceeding.**

## Dependencies
- adventure-scene-contract (need schema before reading act files)
- folder-restructure (need adventures/ path)
