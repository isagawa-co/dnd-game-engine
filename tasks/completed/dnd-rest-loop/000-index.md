# D&D Rest Loop — Task Index

## Goal
Build the rest loop sub-skill: long rest (full recovery), short rest (partial recovery), hit dice recovery, condition removal, interruption mechanics.

## Source
→ [[docs/backlog/014-dnd-build-rest-loop.md]]
→ [[docs/backlog/014-dnd-build-rest-loop/rest-mechanics.md]]

## Tasks

| # | Task | Type | Dependencies | Status |
|---|------|------|-------------|--------|
| 001 | [[001-build-rest-loop-contract]] | BUILD | none | pending |
| 002 | [[002-build-rest-skill-md]] | BUILD | 001 | pending |
| 003 | [[003-build-rest-operations]] | BUILD | 001 | pending |
| 004 | [[004-build-condition-removal]] | BUILD | 001 | pending |
| 005 | [[005-build-interruption]] | BUILD | 001 | pending |
| 006 | [[006-build-tests]] | TEST | 003-005 | pending |
| 007 | [[007-verify-all-gates]] | TEST | 001-006 | pending |

## Gate Contract
→ [[gate-contract.md]]

## Deliverables
- `.claude/skills/rest/SKILL.md` — rest skill definition
- `.claude/skills/rest/rest-loop-contract.json` — input/output contract
- `.claude/skills/rest/rest_operations.py` — long rest, short rest, hit dice recovery
- `.claude/skills/rest/condition_removal.py` — condition removal rules
- `.claude/skills/rest/interruption.py` — location safety, interruption chance
- `.claude/skills/rest/tests/test_rest.py` — L1/L2/L3 tests
