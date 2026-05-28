# Task 006 — Build Narration Generator Reference

## Action
Write `.claude/skills/narration/references/narration-generator.md`

## Acceptance Criteria
- File exists at specified path
- Contains: Narration request flow (receive request → select template → call API or fallback → validate output → return)
- Contains: Caching strategy (cache by narration_type + context hash, TTL 24h, max 1000 entries)
- Contains: Quality validation rules (length 20-100 words, quality_score >= 0.85, tokens <= 200)
- Contains: API configuration (model selection, max_tokens, temperature)
- Contains: Integration dispatch table (which loop calls which narration type)

## Gate
STRUCT-006
