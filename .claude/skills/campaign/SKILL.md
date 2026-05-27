# Campaign Loop — Skill Definition

**Tier:** Level 0 (Campaign Orchestration)

**Identity:** Campaign loop manages the 5-tier state hierarchy and orchestrates gameplay progression from campaign start through arc completion and transition.

## 5-Step Campaign Loop

The campaign loop executes 5 sequential steps per campaign session:

### Step 1: Load Campaign
- Load existing campaign from disk OR initialize new campaign
- Instantiate CampaignState with campaign_id, campaign_name, and metadata
- Create campaign directory structure if needed

### Step 2: Resume Session
- Restore prior session checkpoint or create new session
- Reconstruct all 5 state tiers from checkpoint:
  - Tier 1: Campaign (persists across all arcs)
  - Tier 2: Arc (current story arc state)
  - Tier 3: Session (single play session)
  - Tier 4: Scene (scene within session)
  - Tier 5: Combat (ephemeral combat state)

### Step 3: Play Campaign
- Invoke scene loop to run gameplay
- Track encounters and progression
- Update session and scene state as encounters complete
- Record scene completion in session state

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
4. **Prompt user for action** — what does their character do?
5. **Apply rules** from the contracts and skills to resolve outcomes
6. **Update state** in campaign JSON files
7. **Repeat** until session or game ends

Your role is to read the prescriptive skills and contracts, then MAKE DECISIONS as the Dungeon Master. You don't execute Python code — you understand the D&D rules, read the JSON contracts, and narrate/decide outcomes.
