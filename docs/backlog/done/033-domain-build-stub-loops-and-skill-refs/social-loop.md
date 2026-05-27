# Social Loop

## Status
NEW

## Location
`.claude/skills/social/SKILL.md` + `.claude/skills/social/contracts/`

## What
Social encounter loop for NPC conversations, persuasion, deception, intimidation, and information gathering. Dispatched by scene loop when `encounter_type == "social"` or by state evaluation when `social.active == true`.

## Resolution Flow
1. Receive social encounter from scene loop (NPC id, disposition, topics, DCs)
2. Present NPC and situation to user
3. Offer approach options via action-prompt (persuade, deceive, intimidate, insight, custom)
4. Prompt for Charisma-based check (Persuasion/Deception/Intimidation) or Wisdom (Insight)
5. Compare roll vs DC, apply disposition shift
6. Track information revealed, attitude changes, quest updates
7. Return outcome to scene loop

## Contracts Needed
- `social-action-contract.json` — input: npc_id, approach, skill_used, roll, DC
- `social-outcome-contract.json` — output: disposition_change, information_revealed, quest_updates, attitude (hostile/unfriendly/neutral/friendly/helpful)

## Dependencies
- action-prompt skill (user choices)
- entity system (NPC data, personality, disposition)
- atomic-ops (ability checks)
- campaign state (quest tracking, npcs_met)
