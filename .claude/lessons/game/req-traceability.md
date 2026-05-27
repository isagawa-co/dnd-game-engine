# REQ Traceability

<!-- Seeded: expert knowledge for requirements traceability pattern -->

## The Problem

Without bidirectional traceability between GDD requirements and tests, coverage gaps go undetected. A system can "pass all tests" while missing half the specified behaviors. Orphan tests (no matching REQ) waste execution time.

## Why It Fails

- GDD says "units have movement points" but no test verifies it
- Test exists for "unit can attack" but GDD never specified attack rules
- Coverage report shows "100% test pass rate" — but only tests 40% of REQs
- After a GDD revision, no one knows which tests need updating

## Correct Approach

**Every REQ gets a test. Every test has a REQ. No orphans.**

```
GDD Section → REQ ID → Gate Contract Row → Test Function → Pass/Fail
REQ-COMBAT-001 → COMBAT-01 → test_damage_formula_REQ_COMBAT_001() → PASS
```

**Naming convention:** `test_[descriptive_name]_REQ_[SYSTEM]_[NNN]`

**Coverage script** (`scripts/req-coverage.py`) validates:
1. Extract all REQ IDs from `docs/game-design/sections/*.md`
2. Extract all REQ references from `tests/*.py`
3. Report untested REQs (GDD has it, no test)
4. Report orphan tests (test references REQ not in GDD)
5. Exit 0 only if zero orphans in both directions

**Run coverage after every system build**, not just at the end.

## Source

Design principle from backlog 007: design-principles.md (Requirements Traceability Pattern)
