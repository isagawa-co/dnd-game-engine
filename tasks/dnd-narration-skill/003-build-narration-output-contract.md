# Task 003 — Build Narration Output Contract

## Action
Write `.claude/skills/narration/contracts/narration-output.json`

## Acceptance Criteria
- File exists at specified path
- Valid JSON schema
- Required fields: narration_type, generated_text, length_words
- Optional fields: quality_score, model_used, tokens_used, cached
- narration_type enum matches request contract (6 types)
- length_words: integer, minimum 10, maximum 200
- quality_score: number between 0.0 and 1.0

## Gate
STRUCT-003, CONTENT-003
