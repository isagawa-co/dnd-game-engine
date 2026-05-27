# Social Loop — Skill Definition

## Identity

| Key | Value |
|-----|-------|
| Skill | social |
| Type | sub-loop |
| Parent | scene-loop |
| Purpose | Resolve NPC conversations, persuasion, deception, intimidation, and information gathering |

## Vocabulary

| Term | Definition |
|------|-----------|
| Disposition | NPC attitude toward party: hostile, unfriendly, neutral, friendly, helpful |
| Social Check | Charisma-based ability check (Persuasion, Deception, Intimidation) or Wisdom (Insight) |
| Information | Facts, rumors, or quest hooks revealed through successful social interaction |
| Attitude Shift | Change in NPC disposition based on check results (+1/-1 on the 5-point scale) |

## Contracts

| Contract | File |
|----------|------|
| Input | -> [[contracts/social-action-contract.json]] |
| Output | -> [[contracts/social-outcome-contract.json]] |

## Resolution Flow

1. Scene loop sends social encounter (NPC id, disposition, available topics, DCs)
2. Present NPC description and current situation to user
3. Offer approach options via action-prompt: persuade, deceive, intimidate, insight, custom
4. Prompt user for Charisma-based check (Persuasion/Deception/Intimidation DC) or Wisdom (Insight DC)
5. Compare roll vs DC:
   - Roll >= DC+5: strong success — disposition shifts +1, all topic info revealed
   - Roll >= DC: success — disposition shifts +1, primary info revealed
   - Roll < DC: failure — no shift, no info
   - Roll < DC-5: critical failure — disposition shifts -1, NPC may become hostile
6. Track information revealed, attitude changes, quest updates
7. Return outcome dict to scene loop for state mutation

## Agent Execution

When resolving a social encounter:

1. **Identify the NPC** from the act file's encounter data — use their name, personality, and disposition
2. **Set the scene** — describe the NPC, their demeanor, the environment
3. **Present options** using action-prompt skill with `social` context:
   - Persuade (Persuasion check)
   - Deceive (Deception check)
   - Intimidate (Intimidation check)
   - Read intent (Insight check)
   - Custom approach (player describes, DM assigns skill + DC)
4. **Prompt for roll** — "Make a Persuasion check (DC 12)"
5. **Resolve** — apply the result per the flow above
6. **Narrate outcome** — describe the NPC's reaction, information gained
7. **Update state** — record npcs_met, quest updates, disposition changes

## Integration

- **Depends on:** action-prompt (user choices), entity system (NPC personality/disposition), atomic-ops (ability checks)
- **Returns to:** scene-loop (outcome dict with disposition_change, information_revealed, quest_updates)
- **State updates:** campaign_state.json → npcs_met, quests, npc dispositions
