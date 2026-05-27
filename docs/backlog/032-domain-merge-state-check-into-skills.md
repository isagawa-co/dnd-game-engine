# Merge State Check Into Skill Final Steps

## Status
Open

## Priority
Medium — the state-check skill is currently a separate invocation. Embedding the checklist directly into each loop's final step reduces friction while keeping defense in depth (hook layer remains as backup).

## Summary
Instead of the agent needing to remember to invoke the state-check skill separately, embed the relevant checklist items directly into each loop skill's final step. The combat loop's Step 5 already does this partially. Extend the pattern to social, challenge, rest, travel, and narration skills. The game-state-enforcer hook remains as the hard enforcement backup — this just makes the soft layer automatic rather than opt-in.

## Requirements
- Combat loop Step 5: already has post-combat checklist — verify completeness
- Social loop: add NPC attitude, quest updates, information gained to final step
- Challenge loop: add outcome, condition changes, resource usage to final step
- Rest loop: add HP recovery, slot recovery, ability reset to final step
- Travel loop: add distance, time, random encounters, location update to final step
- Narration skill: add location, time, act progress to final step
- Keep game-state-enforcer.py hook unchanged (hard backup)

## References
- State check skill: `.claude/skills/state-check/SKILL.md`
- Combat loop: `.claude/skills/combat/SKILL.md`
- Game state enforcer: `.claude/hooks/game-state-enforcer.py`

## Task Builder Input
- **Deliverable:** Updated skill files with embedded state check steps
- **Location:** workspace
- **Scope:** REFACTOR
- **Constraints:** Do not remove the state-check skill or hook — this is additive integration
