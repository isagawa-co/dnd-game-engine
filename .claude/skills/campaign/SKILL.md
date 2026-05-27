# Campaign Loop — Skill Definition

**Tier:** Level 0 (Campaign Orchestration)

**Identity:** Campaign loop manages the 5-tier state hierarchy and orchestrates gameplay progression from campaign start through arc completion and transition.

## 5-Step Campaign Loop

The campaign loop executes 5 sequential steps per campaign session:

### Step 1: Load Campaign
- Load existing campaign from disk OR initialize new campaign
- Instantiate CampaignState with campaign_id, campaign_name, and metadata
- Create campaign directory structure if needed

### Step 1.5: Load Adventure (MANDATORY)
- Read `campaign.json` → get `adventure_id` (e.g., `"lmop"`)
- Read `adventures/[adventure_id]/manifest.json` → verify adventure pack exists
- Read `campaign_state.json` → get `current_chapter` and `current_act`
- If current chapter's scene files don't exist under `adventures/[id]/scenes/` → build them from training knowledge before proceeding
- Read the current act file (`adventures/[id]/scenes/chapter-N-*/act-[numeral].json`) → this is the script for this iteration
- **CONSTRAINT: The agent MUST complete this step before any narration. All encounters, NPCs, locations, and plot beats come from the act file. The agent may add flavor text and dialog but MUST NOT invent new encounters, NPCs, or plot points not defined in the act file.**

### Step 2: Resume Session
- Restore prior session checkpoint or create new session
- Reconstruct all 5 state tiers from checkpoint:
  - Tier 1: Campaign (persists across all arcs)
  - Tier 2: Arc (current story arc state)
  - Tier 3: Session (single play session)
  - Tier 4: Scene (scene within session)
  - Tier 5: Combat (ephemeral combat state)

### Step 3: Play Campaign
- Read the current act file loaded in Step 1.5
- Present the `read_aloud` text to the user
- Present action menu using the action-prompt skill with context from the act's encounter data
- Resolve encounters per the act's encounter definitions using monster stat blocks from `adventures/[id]/monsters/`
- Follow `transitions` in the act file to determine the next act when the current one completes
- Update `current_chapter`, `current_act`, and `current_act_id` in campaign state
- **ANTI-DRIFT RULE: Do not narrate events, NPCs, or encounters not defined in the act file. If the player takes an unexpected action, resolve it within the act's context or transition to the appropriate act.**

### Step 4: Check Arc Completion
- Evaluate arc completion conditions via arc-transition module
- Check if arc meets completion criteria (encounter threshold or explicit marking)
- If arc complete: trigger transition to next arc
- If arc ongoing: prepare for next session

### Step 5: Save and Exit
- Persist all state tiers to checkpoint file
- Save campaign state to disk
- Record completion timestamp
- Clean up ephemeral combat state

## Key Principles for Agent Execution

**You are the DM.** Read this skill definition to understand how to orchestrate gameplay:

1. **Load campaign state** from the campaign JSON files
2. **Resolve state** against the state-evaluation contract to determine what happens next
3. **Narrate the situation** to the user based on the current campaign state
4. **Prompt user for action** — use the **action-prompt** skill (`.claude/skills/action-prompt/SKILL.md`) for standardized presentation. Every decision point uses numbered options + custom input.
5. **Apply rules** from the contracts and skills to resolve outcomes
6. **Update state** in campaign JSON files
7. **Repeat** until session or game ends

Your role is to read the prescriptive skills and contracts, then MAKE DECISIONS as the Dungeon Master. You don't execute Python code — you understand the D&D rules, read the JSON contracts, and narrate/decide outcomes.

## Contracts

| Contract | File | Purpose |
|----------|------|---------|
| Campaign Loop | -> [[contracts/campaign-loop-contract.json]] | 5-tier state hierarchy and loop orchestration |
| Campaign Action | -> [[contracts/campaign-action-contract.json]] | Input schema for campaign actions |
| Campaign Outcome | -> [[contracts/campaign-outcome-contract.json]] | Output schema for campaign results |
| Arc Progression | -> [[contracts/arc-progression-contract.json]] | Arc completion conditions and transitions |
| Session Management | -> [[contracts/session-management-contract.json]] | Session save/load/resume contracts |
| State Mutation | -> [[contracts/state-mutation-contract.json]] | Atomic state update rules and validation |

## Action Prompt Integration

At every decision point where the user must choose, read and follow `.claude/skills/action-prompt/SKILL.md`. This ensures consistent presentation across all game loops. See `contracts/action-prompt-contract.json` for context-specific default actions.
