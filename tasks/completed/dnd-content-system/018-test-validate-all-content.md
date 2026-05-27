# Test — Validate All Content Against Schemas

## Context
Validate every content file against its corresponding schema. Verify wiki-link resolution paths. Confirm manifest counts match actual files. This is the L1+L2+L3 validation gate for the entire content system.

## Type
TEST

## Execution
agent

## Dependencies
- 001-017

## Phase Gate
- [ ] All 6 schema files exist in `.claude/skills/content/contracts/`
- [ ] `.claude/skills/content/catalog.json` exists
- [ ] `content/lost-mine-phandelver/manifest.json` exists
- [ ] 24 monster files exist in `content/lost-mine-phandelver/monsters/`
- [ ] 3 spell files exist in `content/lost-mine-phandelver/spells/`
- [ ] 18 item files exist in `content/lost-mine-phandelver/items/`

## Requirements
- Write and run a Python validation script that:
  1. Loads each schema from `contracts/`
  2. Loads each content file from the pack
  3. Validates content against its schema using `jsonschema` library (or manual field check if unavailable)
  4. Verifies all manifest wiki_link entries have corresponding files
  5. Verifies catalog content_count matches manifest array lengths
  6. Reports pass/fail per file with details on failures
- All 45 content files must pass validation
- All wiki-link paths must resolve to existing files
- Catalog counts must match manifest counts

## Acceptance Criteria
- [ ] Validation script runs without error
- [ ] All 24 monster files pass schema validation
- [ ] All 3 spell files pass schema validation
- [ ] All 18 item files pass schema validation
- [ ] Manifest counts match: monsters=24, spells=3, items=18
- [ ] All wiki-link paths resolve to existing files

## Gates Satisfied
- TEST-01, FUNC-07, FUNC-08

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
