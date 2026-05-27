# Gate Contract — D&D Rest Loop

## Gates

| ID | Check | Method | Pass Criteria | Fail Action |
|----|-------|--------|---------------|-------------|
| BUILD-01 | rest-loop-contract.json exists | file_exists | `test -f .claude/skills/rest/rest-loop-contract.json` | Create file |
| BUILD-02 | SKILL.md exists | file_exists | `test -f .claude/skills/rest/SKILL.md` | Create file |
| BUILD-03 | rest_operations.py exists | file_exists | `test -f .claude/skills/rest/rest_operations.py` | Create file |
| BUILD-04 | condition_removal.py exists | file_exists | `test -f .claude/skills/rest/condition_removal.py` | Create file |
| BUILD-05 | interruption.py exists | file_exists | `test -f .claude/skills/rest/interruption.py` | Create file |
| FUNC-01 | long_rest returns recovery dict | run_code | `python -c "from rest_operations import long_rest; r = long_rest({'pcs': [{'id': 'pc-1', 'hp': 5, 'max_hp': 20, 'level': 3, 'hit_die': 'd10', 'con_modifier': 2, 'spell_slots': {}, 'max_spell_slots': {}, 'hit_dice_remaining': 1, 'conditions': []}]}); assert r['result_code'] == 'long_rest_completed'"` | Fix function |
| FUNC-02 | short_rest returns recovery dict | run_code | `python -c "from rest_operations import short_rest; r = short_rest({'pcs': [{'id': 'pc-1', 'hp': 5, 'max_hp': 20, 'level': 3, 'hit_die': 'd10', 'con_modifier': 2, 'hit_dice_remaining': 1, 'conditions': []}]}); assert r['result_code'] == 'short_rest_completed'"` | Fix function |
| FUNC-03 | roll_hit_die returns roll details | run_code | `python -c "from rest_operations import roll_hit_die; r = roll_hit_die('d10', 2); assert 'roll' in r and 'total' in r"` | Fix function |
| FUNC-04 | condition removal works | run_code | `python -c "from condition_removal import remove_conditions_long_rest; r = remove_conditions_long_rest(['exhaustion','poisoned','blinded']); assert 'blinded' in r and 'exhaustion' not in r"` | Fix function |
| FUNC-05 | interruption check works | run_code | `python -c "from interruption import check_interruption; r = check_interruption('safe_inn'); assert r['interrupted'] == False"` | Fix function |
| TEST-01 | All L1 tests pass | run_test | `pytest .claude/skills/rest/tests/test_rest.py -k "l1" --tb=short` exits 0 | Fix imports |
| TEST-02 | All L2 tests pass | run_test | `pytest .claude/skills/rest/tests/test_rest.py -k "l2" --tb=short` exits 0 | Fix execution |
| TEST-03 | All L3 tests pass | run_test | `pytest .claude/skills/rest/tests/test_rest.py -k "l3" --tb=short` exits 0 | Fix correctness |

## Requirements Coverage
Each gate maps to task acceptance criteria. All 7 tasks covered.
