# Challenge Loop — Skill Definition

## Identity

| Key | Value |
|-----|-------|
| Skill | challenge |
| Type | sub-loop |
| Parent | scene-loop |
| Purpose | Resolve environmental obstacles and skill challenges via ability checks |

## Vocabulary

| Term | Definition |
|------|-----------|
| Challenge | A non-combat obstacle requiring an ability check (climb, pick lock, investigate, etc.) |
| DC | Difficulty Class — the target number to meet or exceed |
| Outcome Code | Classification of result: success, partial_success, failure, critical_failure |
| Consequence | Effect applied after resolution (damage, exhaustion, time loss, enemy alert, or none) |

## Contracts

| Contract | File |
|----------|------|
| Input | → [[contracts/challenge-action-contract.json]] |
| Output | → [[contracts/challenge-outcome-contract.json]] |

## Resolution Flow

1. Scene loop sends challenge action (matching input contract)
2. Determine DC from challenge type + difficulty tier
3. Compare roll total vs DC to classify outcome code
4. Apply consequence rules per challenge type and result
5. Assemble full outcome dict and return to scene loop for state mutation and narration

## Challenge Categories

| Category | Types |
|----------|-------|
| Physical | climb, swim, jump, balance, push_pull |
| Stealth | hide, sneak |
| Locks | pick_lock, break_door, disable_trap |
| Knowledge | investigate, arcana, history, religion, nature |
| Perception | perception, insight |

## Agent Execution

When resolving a challenge:

1. **Identify challenge type** from the encounter data
2. **Determine DC** based on the challenge difficulty (easy=10, medium=12, hard=15, very hard=17)
3. **Present approach options** using the **action-prompt** skill (`.claude/skills/action-prompt/SKILL.md`) — show the user how they can attempt the challenge (which skill, which character, creative approaches)
4. **Prompt user for roll** — e.g., "Make an Athletics check (DC 12)" — wait for their d20 roll
5. **Apply the result**:
   - Roll ≥ DC → success (user succeeds at the challenge)
   - Roll < DC → failure (obstacle remains or consequence applies)
6. **Update state** and narrate the outcome to the user

The user provides the actual die roll; you use it to determine success/failure.
