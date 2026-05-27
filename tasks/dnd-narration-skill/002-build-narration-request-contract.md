# Task 002 — Build Narration Request Contract

## Action
Write `.claude/skills/narration/contracts/narration-request.json`

## Acceptance Criteria
- File exists at specified path
- Valid JSON schema
- Required fields: narration_type (enum of 6 types), context (object), tone (enum: epic|dark|humorous|serious)
- narration_type enum: combat_round, combat_victory, social_outcome, challenge_outcome, encounter_setup, loot_discovery
- context object has conditional required fields per narration_type (actor_pc, target_enemy for combat; npc for social; location for encounter_setup; items for loot_discovery)

## Gate
STRUCT-002, CONTENT-002
