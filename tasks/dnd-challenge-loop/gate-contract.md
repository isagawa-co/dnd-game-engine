# Challenge Loop — Gate Contract

## Gates

| Gate ID | Task | Check | Method | Expected |
|---------|------|-------|--------|----------|
| BUILD-01 | 001 | Challenge action contract exists | file_exists | `.claude/skills/challenge/contracts/challenge-action-contract.json` |
| BUILD-02 | 002 | Challenge outcome contract exists | file_exists | `.claude/skills/challenge/contracts/challenge-outcome-contract.json` |
| FUNC-01 | 003 | determine_dc returns int | run_code | `python -c "import sys; sys.path.insert(0,'.claude/skills'); from challenge.challenge_resolution import determine_dc; assert isinstance(determine_dc('climb','moderate'), int)"` |
| FUNC-02 | 003 | resolve_challenge returns dict | run_code | `python -c "import sys; sys.path.insert(0,'.claude/skills'); from challenge.challenge_resolution import resolve_challenge; r=resolve_challenge({'challenge_type':'climb','actor_pc':'pc-1','skill_used':'athletics','difficulty_class':12,'roll_result':{'d20_roll':15,'modifiers_total':4,'total':19}}); assert isinstance(r, dict) and 'success' in r"` |
| FUNC-03 | 003 | compute_outcome_code classifies correctly | run_code | `python -c "import sys; sys.path.insert(0,'.claude/skills'); from challenge.challenge_resolution import compute_outcome_code; assert compute_outcome_code(19, 12) == 'success'; assert compute_outcome_code(11, 12) == 'partial_success'; assert compute_outcome_code(8, 12) == 'failure'"` |
| BUILD-03 | 004 | SKILL.md exists | file_exists | `.claude/skills/challenge/SKILL.md` |
| TEST-01 | 005 | All tests pass | run_test | `python -m pytest .claude/skills/challenge/tests/test_challenge_resolution.py -v --rootdir=.` |
| TEST-02 | 005 | At least 12 tests exist | run_code | `python -c "import subprocess; r=subprocess.run(['python','-m','pytest','.claude/skills/challenge/tests/test_challenge_resolution.py','--collect-only','-q','--rootdir=.'],capture_output=True,text=True); lines=[l for l in r.stdout.strip().split('\n') if '::' in l]; assert len(lines) >= 12, f'Only {len(lines)} tests found'"` |
