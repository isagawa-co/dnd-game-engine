# Granularity Reference — Atomic Task Decomposition

## Why This Exists

Task-builder repeatedly produces fat tasks (multiple actions bundled into one task file) despite RULE ZERO corrections. The root cause: the existing rules say "one task = one action" but don't show what that looks like concretely. The agent interprets "one action" differently depending on context. This reference eliminates ambiguity with concrete before/after examples.

## Core Principle

**Each task = one `claude -p` invocation = one action = one checkpoint.**

A completed task is committed to `completed_tasks` in workflow state. The next `claude -p` skips it. If the current task fails, only that one action is lost. This is the mechanism that makes the architecture reliable.

## Why It Matters (the agent must understand this)

```
Fat tasks:    10 tasks × 4 actions each = 10 claude -p calls, each doing 4 things
              If task 3 fails at action 2: actions 1-2 done but task marked failed
              Resume retries entire task — may redo completed work
              Blast radius: 4 actions

Atomic tasks: 40 tasks × 1 action each = 40 claude -p calls, each doing 1 thing
              If task 12 fails: task 12 retried, tasks 1-11 already committed
              Blast radius: 1 action
```

Five reasons granularity is architectural, not stylistic:
1. **Failure isolation** — one task fails, one task retries
2. **Context efficiency** — each agent gets a small, focused job that fits in context
3. **Progress durability** — completed tasks survive crashes, timeouts, zombie processes
4. **Provenance clarity** — one task → one artifact → one hash → one Rekor entry
5. **Parallelism readiness** — independent atomic tasks can eventually run in parallel

## The Decision Test

When writing a task, ask: **"If this task times out at 600s with no output, how much work is lost?"**

- If the answer is "one file" → correct granularity
- If the answer is "three files and a config change" → too fat, split it

## Concrete Examples — Before and After

### Example 1: Writing multiple source files

**BAD — fat task:**
```markdown
# 005-build-write-validators.md
## Requirements
- Write `validators/ssh_validator.py` with SSHValidator class
- Write `validators/config_loader.py` with ConfigLoader class
- Write `validators/__init__.py` with imports
- Write `tests/test_ssh_validator.py` with 3 test cases
```

**GOOD — atomic tasks:**
```markdown
# 005-build-write-ssh-validator.md
## Requirements
- Write `validators/ssh_validator.py` with SSHValidator class
## Acceptance Criteria
- [ ] `validators/ssh_validator.py` exists
- [ ] File contains `class SSHValidator`

# 006-build-write-config-loader.md
## Requirements
- Write `validators/config_loader.py` with ConfigLoader class
## Acceptance Criteria
- [ ] `validators/config_loader.py` exists
- [ ] File contains `class ConfigLoader`

# 007-build-write-validators-init.md
## Requirements
- Write `validators/__init__.py` importing SSHValidator and ConfigLoader
## Acceptance Criteria
- [ ] `validators/__init__.py` exists
- [ ] File contains `from .ssh_validator import SSHValidator`

# 008-test-write-ssh-validator-tests.md
## Requirements
- Write `tests/test_ssh_validator.py` with test cases for SSHValidator
## Acceptance Criteria
- [ ] `tests/test_ssh_validator.py` exists
- [ ] File contains at least 3 test functions
```

### Example 2: Setting up infrastructure

**BAD — fat task:**
```markdown
# 001-build-setup-project.md
## Requirements
- Create project directory
- Initialize git repo
- Write README.md
- Write .gitignore
- Write requirements.txt
- Install dependencies
```

**GOOD — atomic tasks:**
```markdown
# 001-build-create-project-dir.md
## Requirements
- Create directory at `D:\my_ai_projects\project-name`
## Acceptance Criteria
- [ ] Directory exists

# 002-build-git-init.md
## Requirements
- Run `git init` in the project directory
## Acceptance Criteria
- [ ] `.git/` directory exists

# 003-build-write-readme.md
## Requirements
- Write `README.md` with project title and description
## Acceptance Criteria
- [ ] `README.md` exists
- [ ] File contains `# Project Name`

# 004-build-write-gitignore.md
## Requirements
- Write `.gitignore` with Python defaults
## Acceptance Criteria
- [ ] `.gitignore` exists

# 005-build-write-requirements.md
## Requirements
- Write `requirements.txt` with project dependencies
## Acceptance Criteria
- [ ] `requirements.txt` exists

# 006-build-install-deps.md
## Requirements
- Run `pip install -r requirements.txt`
## Acceptance Criteria
- [ ] `pip install` exits 0
```

### Example 3: Testing with setup

**BAD — fat task:**
```markdown
# 020-test-run-full-suite.md
## Requirements
- Create test fixtures directory
- Copy test input files
- Set environment variables
- Run pytest
- Verify all tests pass
```

**GOOD — atomic tasks:**
```markdown
# 020-test-create-fixtures-dir.md
## Requirements
- Create `tests/fixtures/` directory
## Acceptance Criteria
- [ ] `tests/fixtures/` directory exists

# 021-test-write-input-fixtures.md
## Requirements
- Write `tests/fixtures/valid_config.json` with test SSH config
## Acceptance Criteria
- [ ] `tests/fixtures/valid_config.json` exists
- [ ] File is valid JSON

# 022-test-run-pytest.md
## Requirements
- Run `pytest tests/ -v`
## Acceptance Criteria
- [ ] pytest exits 0
- [ ] All test functions pass
```

### Example 4: Editing existing files

**BAD — fat task:**
```markdown
# 010-build-update-pipeline.md
## Requirements
- Add attestation import to `attest.py`
- Add intent_chain parameter to `schema.py` create_bundle()
- Update `backlog.md` command to call intent.py
- Update `SKILL.md` step table
```

**GOOD — atomic tasks:**
```markdown
# 010-build-update-attest-import.md
## Requirements
- Add `from intent import read_intent_chain` to `lib/attestation/attest.py`
## Acceptance Criteria
- [ ] `attest.py` contains `from intent import read_intent_chain`

# 011-build-update-schema-intent-param.md
## Requirements
- Add `intent_chain: Optional[List[dict]] = None` parameter to `create_bundle()` in `lib/attestation/schema.py`
## Acceptance Criteria
- [ ] `schema.py` `create_bundle` function signature includes `intent_chain`

# 012-build-update-backlog-command.md
## Requirements
- Add step 3 "Record intent" to `.claude/commands/kernel/backlog.md`
## Acceptance Criteria
- [ ] `backlog.md` contains `## 3. Record intent` or equivalent step

# 013-build-update-skill-step-table.md
## Requirements
- Update step table in `SKILL.md` to reflect new step numbering
## Acceptance Criteria
- [ ] `SKILL.md` step table matches current step files
```

## Edge Cases

### "But this file is only 3 lines"
A task that writes a 3-line `__init__.py` IS a valid task. It takes one `claude -p` agent 30 seconds. That's correct. The alternative — bundling it with 4 other file writes — means if anything fails, all 5 are retried.

### "These two changes are in the same file"
Still two tasks if they're logically independent changes. Example: adding an import AND adding a new function. If the import is wrong, you don't want to re-add the function. Exception: if change B literally cannot exist without change A (e.g., import + usage in the same function), they can be one task.

### "It's just a config change"
One config change = one task. `pip install` = one task. `git init` = one task. `mkdir` = one task. These complete in seconds. That's the point.

### "There are 80 tasks now"
80 tasks is correct if the work has 80 actions. The number of tasks is driven by the work, not an arbitrary cap. 80 atomic tasks that each complete in 30-60 seconds is better than 20 fat tasks that each take 5-8 minutes and might fail at step 3 of 4.

## How to Count

When decomposing, count the verbs:
- "Write file A" → 1 task
- "Write file A and file B" → 2 tasks
- "Write file A, then run tests" → 2 tasks
- "Create directory, write config, install deps" → 3 tasks
- "Edit file A to add import, add function, add tests" → 3 tasks (if independent)

**If the Requirements section has bullet points, each bullet is probably a task.**
