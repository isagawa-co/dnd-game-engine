# Task 001 — Build Narration SKILL.md

## Action
Write `.claude/skills/narration/SKILL.md`

## Acceptance Criteria
- File exists at specified path
- Contains: Type, Domain, What section
- Contains: Architecture section describing narration request/output flow
- Contains: wiki-links to all contracts (`[[contracts/narration-request.json]]`, `[[contracts/narration-output.json]]`)
- Contains: wiki-links to all references (`[[references/prompt-templates.md]]`, `[[references/fallback-templates.md]]`, `[[references/narration-generator.md]]`)
- Contains: Narration Types table (6 types: combat_round, combat_victory, social_outcome, challenge_outcome, encounter_setup, loot_discovery)
- Contains: Integration Points section (combat-loop 010, social-loop 011, challenge-loop 012, scene-loop 007)
- Contains: Quality Thresholds table
- Contains: Error Handling table

## Gate
STRUCT-001, CONTENT-001
