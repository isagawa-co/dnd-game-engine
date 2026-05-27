# Gate Contract — dnd-narration-skill

**Backlog:** 017-dnd-build-narration-skill

## Structure Gates

| ID | Check | Verification |
|----|-------|-------------|
| STRUCT-001 | SKILL.md exists at `.claude/skills/narration/SKILL.md` | `ls projects/ai-dnd-game/.claude/skills/narration/SKILL.md` |
| STRUCT-002 | Request contract exists | `ls projects/ai-dnd-game/.claude/skills/narration/contracts/narration-request.json` |
| STRUCT-003 | Output contract exists | `ls projects/ai-dnd-game/.claude/skills/narration/contracts/narration-output.json` |
| STRUCT-004 | Prompt templates reference exists | `ls projects/ai-dnd-game/.claude/skills/narration/references/prompt-templates.md` |
| STRUCT-005 | Fallback templates reference exists | `ls projects/ai-dnd-game/.claude/skills/narration/references/fallback-templates.md` |
| STRUCT-006 | Narration generator reference exists | `ls projects/ai-dnd-game/.claude/skills/narration/references/narration-generator.md` |

## Content Gates

| ID | Check | Verification |
|----|-------|-------------|
| CONTENT-001 | SKILL.md has wiki-links to all contracts and references | grep for `[[` links in SKILL.md |
| CONTENT-002 | Request contract covers all 6 narration types | grep narration_type enum in request contract |
| CONTENT-003 | Output contract has required fields (narration_type, generated_text, length_words) | grep fields in output contract |
| CONTENT-004 | Prompt templates cover combat_round, social_outcome, encounter_setup, loot_discovery | grep template names |
| CONTENT-005 | Fallback templates cover all 6 narration types | grep fallback entries |

## Test Gates

| ID | Check | Verification |
|----|-------|-------------|
| TEST-001 | Test file exists | `ls projects/ai-dnd-game/tests/test_narration_skill.py` |
| TEST-002 | Tests pass | `python -m pytest projects/ai-dnd-game/tests/test_narration_skill.py -v` |
| TEST-003 | At least 5 tests defined | count test functions |
