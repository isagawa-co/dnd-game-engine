# Execute Pipeline — Skill

**Type:** Prescriptive
**Style:** Indexed — SKILL.md + references/

## What

Takes a user goal (natural language or existing backlog item) and runs the full autonomous pipeline: create backlog → decompose into tasks → execute via run-task.sh. No pause points, no plan approval, fully autonomous under kernel governance.

## Usage

```
/kernel/execute-pipeline Create hmsa-healthcare-qa workspace with kernel + spec + features
/kernel/execute-pipeline docs/backlog/031-domain-build-hmsa-healthcare-qa-workspace.md
/kernel/execute-pipeline 031
```

**Arguments:**
- Natural language goal → creates backlog item, then decomposes and executes
- Backlog file path → skips backlog creation, goes straight to decompose and execute
- Number shorthand (e.g., `031`) → resolves to `docs/backlog/031-*.md`

## Steps

| Step | Action | Reference |
|------|--------|-----------|
| 1 | Parse input (detect mode) | → `references/step-01-parse-input.md` |
| 2 | Create backlog item (skip if existing) | → `references/step-02-create-backlog.md` |
| 3 | Run task-builder (with flags) | → `references/step-03-run-task-builder.md` |
| 4 | Execute tasks via run-task.sh | → `references/step-04-execute-tasks.md` |
| 5 | Validate + report | → `references/step-05-validate-report.md` |

## Execution

1. **Check for resume state:**
   - Read `.claude/state/session_state.json`
   - If `pipeline_state` exists with `resume_step`, skip to that step

2. **Execute steps sequentially:**
   - Read each reference file before executing that step
   - Each step produces state the next step consumes (via `pipeline_state` in session_state.json)

## Key Principles

- **Fully autonomous** — no pause points, no plan approval, no user confirmation
- **Outer-agent pattern** — same as prod-test: outer agent orchestrates, spawns run-task.sh
- **run-task.sh outside the loop** — tasks execute as one-shot `claude -p` invocations
- **All context passes through** — natural language → backlog → task-builder input, verbatim
- **Kernel-governed** — outer agent follows session-start, anchor, the full loop
- **Composable** — callable standalone or by other commands
- **Flag-based handoff** — sets `pipeline_mode` flags so task-builder skips review and stops before execute

## Pipeline State

State is tracked in `pipeline_state` within `session_state.json`:

```json
{
  "pipeline_state": {
    "input_mode": "existing_backlog | natural_language",
    "backlog_path": "docs/backlog/NNN-*.md",
    "task_folder": "tasks/[project-name]/",
    "task_count": N,
    "resume_step": null
  }
}
```

## Outcome

After completion:
- Backlog item exists (created or pre-existing)
- Task folder with numbered tasks + gate contract
- All tasks executed via run-task.sh
- Validation report produced
- Pipeline state cleared from session_state.json
