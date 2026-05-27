# /kernel/task-builder

Decompose a goal into tasks and execute them autonomously.

## Usage

```
/kernel/task-builder Build the RAGA eval spec using DeepEval as template
/kernel/task-builder Create run-task-batch.sh for batch task execution
```

## Instructions

This command uses a skill-based approach with 10 steps.

### Load Skill

Read and follow: `.claude/skills/task-builder/SKILL.md`

### Quick Reference

| Step | Action |
|------|--------|
| 1 | Parse goal |
| 2 | Research context |
| 3 | Convention check |
| 4 | Resolve template |
| 5 | Decompose into main tasks |
| 6 | Atomize + gate contract |
| 7 | Plan review |
| 8 | Write task files |
| 9 | Execute (start cycling) |
| 10 | Structural audit |

### Key Principles

- **Goal → Main Tasks → Atomic Subtasks** — three-tier decomposition
- **Convention check** — verify directory patterns against sibling platforms in both orgs before building
- **Template resolution** — platform builds read the template repo, produce `_context/` files
- **Path provenance** — every BUILD path traces to `_context/path-mapping.json`
- **Plan review** — present full plan to user for approval before writing task files
- **Index file** — 000-index.md links all tasks
- **Self-contained tasks** — each task implementable alone
- **Testable criteria** — every acceptance criterion is mechanical
- **Structural audit** — post-execution diff against template before shipping
- **Auto-execute** — after plan approval, build and cycle without asking
