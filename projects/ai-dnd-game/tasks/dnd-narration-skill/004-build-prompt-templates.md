# Task 004 — Build Prompt Templates Reference

## Action
Write `projects/ai-dnd-game/.claude/skills/narration/references/prompt-templates.md`

## Acceptance Criteria
- File exists at specified path
- Contains prompt template for each narration type:
  - Combat Round Template (actor, action, result, damage, tone)
  - Combat Victory Template (party_names, defeated_enemies, party_actions, tone)
  - Social Outcome Template (npc_name, social_action, result_code, relationship_change)
  - Challenge Outcome Template (actor, obstacle, method/consequence)
  - Encounter Setup Template (location, terrain, enemies, atmosphere)
  - Loot Discovery Template (items, location, context)
- Each template has: system prompt, user prompt with placeholders, expected output format
- Templates specify word count target (20-100 words)

## Gate
STRUCT-004, CONTENT-004
