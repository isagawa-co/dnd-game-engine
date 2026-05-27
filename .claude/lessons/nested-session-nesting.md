# Nested Session Nesting

## Issue
Running `run-task.sh` from an interactive Claude Code session fails because `CLAUDECODE=1` env var blocks nested `claude -p` invocations.

## Root Cause
Interactive Claude Code sets `CLAUDECODE=1`. When `run-task.sh` calls `claude -p`, the env var is inherited and blocks the nested session.

## Wrong Fix (2026-04-28 — corrected)
Previously: "Use Agent tool with `run_in_background: true`" — this was WRONG. The Agent tool itself runs as `claude -p`, so running `env -u CLAUDECODE bash run-task.sh` inside an Agent creates **double nesting**: interactive session → Agent (`claude -p`) → run-task.sh → `claude -p`. The inner `claude -p` fails silently. Symptoms: 0 bytes output file, no iteration logs created, agent shows "running" status indefinitely.

## Correct Fix
Use **Bash tool with `run_in_background: true`**:
```
Bash(command: 'env -u CLAUDECODE bash run-task.sh [repo] [iterations] [subfolder]', run_in_background: true)
```

This creates only one level of nesting: interactive session → background shell → run-task.sh → `claude -p`. The `env -u CLAUDECODE` strips the blocking var, and the background shell is a raw process (not another `claude -p`), so there's no double-nesting.

## Evidence
- 2026-04-28: Agent tool with `run_in_background` ran for 4+ minutes, produced 0 bytes output, no iteration logs. Stopped and relaunched via Bash `run_in_background` — first iteration started within 30 seconds.

## Key Distinction
| Tool | What it spawns | Can nest claude -p? |
|------|---------------|---------------------|
| Bash `run_in_background` | Raw shell process | YES — only 1 level of nesting |
| Agent `run_in_background` | `claude -p` subprocess | NO — creates 2 levels of nesting, inner one fails silently |

## Anti-Pattern
```
# WRONG — Agent nests claude -p inside claude -p
Agent(prompt: "run env -u CLAUDECODE bash run-task.sh ...", run_in_background: true)
```

## Correct Pattern
```
# RIGHT — Bash spawns raw shell, only 1 level of claude -p nesting
Bash(command: "env -u CLAUDECODE bash run-task.sh ...", run_in_background: true)
```
