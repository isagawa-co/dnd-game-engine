---
name: game-engine-gates
type: gate-contract
parent: game-engine
---

# Game Engine — Gate Contract

## Verification Methods

| Method | How orchestrator checks |
|--------|------------------------|
| `file_exists` | `test -f {{path}}` — does the file exist? |
| `grep` | Search file content for a specific pattern |
| `run_code` | Execute a command and check exit code (0 = pass) |
| `run_test` | Run test suite and check exit code |
| `manual` | Orchestrator reads content and judges (LLM-evaluated) |

## Phase 1 Gates — GDD Quality

| ID | Check | Method | Pass Criteria | Fail Action |
|----|-------|--------|---------------|-------------|
| GDD-01 | Game profile exists | `file_exists` | `docs/game-design/profile.md` exists | Run Step 1 discovery |
| GDD-02 | Profile has genre | `grep` | `profile.md` contains `genre:` | Add genre to profile |
| GDD-03 | Profile has platform | `grep` | `profile.md` contains `platform:` | Add platform to profile |
| GDD-04 | GDD index exists | `file_exists` | `docs/game-design/index.md` exists | Create index from completed sections |
| GDD-05 | Section files exist | `run_code` | `ls docs/game-design/sections/*.md` exits 0 | Run Step 3 section walkthrough |
| GDD-06 | No partial sections remain | `run_code` | `ls docs/game-design/sections/*.partial.md 2>/dev/null` exits non-zero | Complete or remove partial sections |
| GDD-07 | Each section has REQ IDs | `grep` | Every `sections/*.md` contains `REQ-` | Add REQ IDs to sections missing them |
| GDD-08 | REQ IDs follow format | `grep` | All REQ IDs match `REQ-[A-Z]+-[0-9]+` pattern | Fix malformed REQ IDs |
| GDD-09 | Sections have data tables | `manual` | Each section contains concrete values (tables, formulas, enumerations), not vague descriptions | Re-enter discovery for vague sections |

## Phase Transition Gate

| ID | Check | Method | Pass Criteria | Fail Action |
|----|-------|--------|---------------|-------------|
| TRANS-01 | All applicable sections complete | `run_code` | Count of `sections/*.md` (non-partial) == count in state `gdd_sections_applicable` | Report missing sections, resume /game-create |
| TRANS-02 | Profile approved | `grep` | State file contains `"game_profile_approved": true` | Return to Step 1 for profile approval |
| TRANS-03 | No partial files | `run_code` | `find docs/game-design/sections/ -name "*.partial.md"` returns empty | Complete partial sections |

## Phase 2 Gates — Decomposition

| ID | Check | Method | Pass Criteria | Fail Action |
|----|-------|--------|---------------|-------------|
| DECOMP-01 | Backlog items generated | `run_code` | `ls backlog/*.md` exits 0, at least 2 items | Re-read GDD, identify systems |
| DECOMP-02 | Each item references GDD section | `grep` | Every backlog item contains `GDD Section:` | Add GDD section references |
| DECOMP-03 | Dependency order documented | `grep` | Index or first backlog item contains dependency ordering | Add dependency graph to index |
| DECOMP-04 | Each item has REQ IDs | `grep` | Every backlog item contains `REQ-` | Pull REQ IDs from corresponding GDD section |

## Phase 3 Gates — Build Quality

| ID | Check | Method | Pass Criteria | Fail Action |
|----|-------|--------|---------------|-------------|
| BUILD-01 | Source files created | `run_code` | `ls src/**/*.py` (or platform equivalent) exits 0 | Execute next backlog item |
| BUILD-02 | Test files exist | `run_code` | `ls tests/**/*test*.py` (or equivalent) exits 0 | Create tests for implemented REQs |
| BUILD-03 | Test names include REQ IDs | `grep` | Test files contain `REQ-` in function/describe names | Rename tests to include REQ IDs |
| BUILD-04 | Config not hardcoded | `grep` | Balance levers in `config/` or `*.yaml`, not in source | Extract hardcoded values to config |

## REQ Coverage Gates

| ID | Check | Method | Pass Criteria | Fail Action |
|----|-------|--------|---------------|-------------|
| COV-01 | Coverage script exists | `file_exists` | `scripts/req-coverage.py` exists | Generate coverage script |
| COV-02 | All GDD REQs have tests | `run_code` | `python scripts/req-coverage.py` exits 0, no orphan REQs | Write missing tests |
| COV-03 | No orphan tests | `run_code` | Coverage report shows 0 tests without matching REQ | Remove or link orphan tests |

## Test Gates

| ID | Check | Method | Pass Criteria | Fail Action |
|----|-------|--------|---------------|-------------|
| TEST-01 | Test suite passes | `run_test` | `pytest tests/ -v` (or platform equivalent) exits 0 | Fix failing tests using GDD as spec |

## Requirements Registry

| REQ ID | Behavior | GDD Section | Test Name Pattern |
|--------|----------|-------------|-------------------|
| REQ-LOOP-NNN | Game loop behaviors | 01-game-loop | `test_game_loop_*[REQ-LOOP-NNN]` |
| REQ-WORLD-NNN | World/map behaviors | 02-world-space | `test_world_*[REQ-WORLD-NNN]` |
| REQ-ENT-NNN | Entity behaviors | 03-entities | `test_entity_*[REQ-ENT-NNN]` |
| REQ-ACT-NNN | Player action behaviors | 04-player-actions | `test_action_*[REQ-ACT-NNN]` |
| REQ-RULE-NNN | Rules/mechanics behaviors | 05-rules-mechanics | `test_rules_*[REQ-RULE-NNN]` |
| REQ-PROG-NNN | Progression behaviors | 06-progression | `test_progression_*[REQ-PROG-NNN]` |
| REQ-COMBAT-NNN | Combat behaviors | 07-combat | `test_combat_*[REQ-COMBAT-NNN]` |
| REQ-AI-NNN | AI behaviors | 08-ai-opponents | `test_ai_*[REQ-AI-NNN]` |
| REQ-DATA-NNN | External data behaviors | Data sections | `test_data_*[REQ-DATA-NNN]` |

Specific REQ IDs are generated during Phase 1 discovery and populated into this registry as each GDD section is completed.

## Autonomy Rules

- **Fully autonomous:** Phase 2 decomposition, Phase 3 build execution, test runs, coverage checks
- **Requires user approval:** Phase 1 discovery answers (HITL gates), GDD section approval, profile approval
- **Default retries:** 3 per gate failure before escalation
- **Escalation:** Report failing gate + attempted fixes, ask user for direction

## Stop Conditions

- Phase 1: Stop when user pauses or all applicable sections approved
- Phase 2: Stop on circular dependency (escalate to user)
- Phase 3: Stop after 3 consecutive failures on same REQ (escalate to user)
- Any phase: Stop if coverage drops below previous checkpoint
