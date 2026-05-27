# Task 005 — Build Fallback Templates Reference

## Action
Write `.claude/skills/narration/references/fallback-templates.md`

## Acceptance Criteria
- File exists at specified path
- Contains template-based fallback for each narration type (6 types)
- Fallback templates use simple string interpolation: `{actor}`, `{target}`, `{weapon}`, `{damage}`, `{npc}`, etc.
- Each fallback has: hit/miss/success/failure variants as applicable
- Contains: When to use (API unavailable, rate limited, timeout)
- Contains: Graceful degradation rules (game continues with template text)

## Gate
STRUCT-005, CONTENT-005
