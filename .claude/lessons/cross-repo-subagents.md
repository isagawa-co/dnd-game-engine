# Cross-Repo Sub-Agents

## 2026-04-28 Sub-Agent CWD Inheritance

- **Issue:** Playtest sub-agent spawned via Agent tool reported "no team packs, no playbooks, no data" — all files missing. But 32 team packs, playbooks, and full data directory existed in the target repo.
- **Root Cause:** The Agent tool spawns sub-agents in the PARENT's working directory (`game-dev/`), not the target repo (`ai-football-head-coach-sim/`). The sub-agent's Glob, Bash, and directory listing tools all resolve relative to cwd. Absolute path instructions in the prompt were ignored — the agent reverted to relative paths for its checks despite being told 5+ times to use absolute paths.
- **Fix:** Use `Bash(run_in_background: true)` with `cd [target_repo] && env -u CLAUDECODE claude -p "..."`. The `cd` inside a background subprocess is safe — it only affects that subprocess, not the interactive session's cwd or hooks.
- **Anti-Pattern Added:** Never rely on prompt instructions ("use absolute paths") to override cwd for sub-agents. Prompt-level path instructions are unreliable.
- **Quality Gate Added:** When spawning a sub-agent for a different repo, verify it uses `cd [repo] && claude -p` in a background Bash call.

## 2026-04-28 --cwd Does Not Exist

- **Issue:** `claude -p --cwd` fails with `error: unknown option '--cwd'`
- **Root Cause:** The `--cwd` flag does not exist in the Claude CLI. It was assumed to exist based on other CLI patterns.
- **Fix:** Use `cd [target_repo] && env -u CLAUDECODE claude -p "..."` inside a background Bash call. The `cd` is safe because it's in a subprocess.

## Evidence

Three attempts failed with the same root cause:
1. Agent spawned with relative paths → found nothing
2. Agent spawned with explicit absolute paths in prompt → still used relative for Glob/Bash
3. `claude -p --cwd` → `error: unknown option '--cwd'`
4. `cd [repo] && env -u CLAUDECODE claude -p` → SUCCESS

## Correct Pattern

```bash
# WRONG — agent inherits parent cwd, absolute paths in prompt unreliable
Agent(prompt="Read D:/target-repo/packs/teams/...")

# WRONG — --cwd flag doesn't exist
Bash(command: 'env -u CLAUDECODE claude -p --cwd "D:/target-repo" "prompt"')

# RIGHT — cd in background subprocess is safe, doesn't affect parent session
Bash(command: 'cd "D:/target-repo" && env -u CLAUDECODE claude -p "prompt"', run_in_background: true)
```
