# /kernel/execute-pipeline

Fully autonomous pipeline: backlog → task-builder → run-task.sh. One command, idea to done.

## Usage

```
/kernel/execute-pipeline Create hmsa-healthcare-qa workspace with kernel + spec + features
/kernel/execute-pipeline docs/backlog/031-domain-build-hmsa-healthcare-qa-workspace.md
/kernel/execute-pipeline 031
```

## Instructions

This command uses a skill-based approach with 5 steps.

### Load Skill

Read and follow: `.claude/skills/execute-pipeline/SKILL.md`

### Quick Reference

| Step | Action |
|------|--------|
| 1 | Parse input (existing backlog or natural language) |
| 2 | Create backlog item (skip if existing) |
| 3 | Run task-builder (skip review, stop before execute) |
| 4 | Execute tasks via run-task.sh |
| 5 | Validate + report |

### Key Principles

- **Fully autonomous** — no pause points, no plan approval
- **Outer-agent pattern** — orchestrates, spawns run-task.sh as subprocess
- **run-task.sh outside the loop** — each task is a fresh `claude -p` under kernel governance
- **All context passes through** — natural language → backlog → tasks, verbatim
- **Flag-based handoff** — sets `pipeline_mode` so task-builder skips review and defers execution
- **Composable** — callable standalone or by other commands

### Input Modes

| Input | Mode | Example |
|-------|------|---------|
| Natural language | Creates backlog first | `Create a new QA platform for mobile testing` |
| Backlog file path | Skips backlog creation | `docs/backlog/031-domain-build-hmsa-healthcare-qa-workspace.md` |
| Number shorthand | Resolves to backlog file | `031` |
