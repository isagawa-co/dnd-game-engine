# Step 4: Execute Tasks — Classify-Then-Route Dispatch

Execute tasks from the task folder using a classify-then-route pattern. Simple tasks run inline via autonomous-cycle. Complex tasks run isolated via run-task.sh.

## Process

1. **Read pipeline state:**
   - `pipeline_state.task_folder` — e.g., `tasks/vietnam-flights/`
   - `pipeline_state.task_count` — number of tasks to execute
   - `pipeline_state.backlog_path` — backlog file path (for move-to-done)

2. **Extract task subfolder name:**
   - From `tasks/vietnam-flights/` → subfolder is `vietnam-flights`

3. **Classify each task:**

   Read each task file in the folder (excluding `000-index.md` and `gate-contract.md`). For each task, determine its weight:

   ### Classification Heuristic

   Classification is about **task weight**, not task type. Works equally for BUILD, RESEARCH, TEST, and verify tasks.

   **Simple task** (route to autonomous-cycle):
   - 3 or fewer acceptance criteria
   - Single file deliverable (one Write or one Edit)
   - No external dependencies, no infrastructure setup
   - No commands that spawn processes or install packages

   **Complex task** (route to run-task.sh):
   - 4+ acceptance criteria
   - Multi-file deliverable
   - References external services, Docker, APIs
   - Contains keywords: "docker", "install", "infrastructure", "spawn", "run-task.sh", "external", "API", "multiple files"
   - Requires process isolation (tests that need clean state, restarts)

   **Default: complex** — when uncertain, route to run-task.sh (safe fallback). The overhead of spawning `claude -p` (~30s) is cheaper than a crashed inline task losing all progress.

   Produce a classification summary:
   ```
   Task classification:
   - 001-build-edit-config.md → simple (2 criteria, single edit)
   - 002-build-write-module.md → simple (3 criteria, single file)
   - 003-test-run-suite.md → complex (runs pytest, needs isolation)
   - ...
   Simple: N tasks (will run inline)
   Complex: M tasks (will run via run-task.sh)
   ```

4. **Execute simple tasks inline (autonomous-cycle):**

   For each task classified as simple, execute it directly in the current session:
   - Read the task file
   - Implement it (write/edit the file, run the command)
   - Verify acceptance criteria
   - Mark complete via `/kernel/complete`
   - Move to next simple task

   Simple tasks run sequentially in the outer agent's session. No process spawning, no timeout overhead. The outer agent does the work directly.

5. **Execute complex tasks via run-task.sh:**

   After all simple tasks are done, spawn run-task.sh for the remaining complex tasks:

   Use the Agent tool with `run_in_background: true`:

   ```
   Agent(
     description: "Execute [subfolder] complex tasks via run-task.sh",
     prompt: "Run the following bash command and return the full output:
       env -u CLAUDECODE bash \"[repo_path]/run-task.sh\" \"[repo_path]\" [remaining_count + 2] [subfolder] [backlog_path]
       Wait for completion and return the full output including the final status banner.",
     run_in_background: true
   )
   ```

   **4th argument `[backlog_path]`:** Enables automatic move-to-done on ALL_TASKS_COMPLETE. run-task.sh moves the backlog to `docs/backlog/done/` and the task folder to `tasks/completed/`.

   **Why `env -u CLAUDECODE`:** Interactive sessions set `CLAUDECODE=1` which blocks nested `claude -p`. `env -u CLAUDECODE` strips this env var for the subprocess only.

   **Why background Agent:** Creates a decoupled subprocess. Runs autonomously while the interactive session remains responsive.

   run-task.sh spawns one `claude -p` agent per task, sequentially:
   - Each agent reads CLAUDE.md, does session-start + anchor
   - Picks the next incomplete task (skips already-completed simple tasks)
   - Executes it, verifies acceptance criteria
   - Marks complete via /kernel/complete
   - Exits

6. **Wait for notification:**
   - The background agent will notify when complete
   - Do NOT poll — you will be notified automatically

7. **Read results:**
   - Check the agent's returned output for ALL_TASKS_COMPLETE or errors
   - Read workflow state: `completed_tasks`, `skipped_tasks`
   - Read logs at `.claude/state/` if available

8. **Update pipeline state:**
   ```json
   {
     "pipeline_state": {
       "execution_exit_code": 0,
       "completed_count": N,
       "skipped_count": M,
       "simple_inline": S,
       "complex_spawned": C
     }
   }
   ```

## When All Tasks Are Simple

If classification determines ALL tasks are simple, skip run-task.sh entirely. Execute everything inline via autonomous-cycle pattern. This is the fast path — no process spawning overhead at all.

After all inline tasks complete, the outer agent handles move-to-done directly (instead of relying on run-task.sh).

## When All Tasks Are Complex

If classification determines ALL tasks are complex, skip the inline phase. Spawn run-task.sh immediately with all tasks. This is the current (pre-gap-7) behavior.

## Failure Handling

| Outcome | Action |
|---------|--------|
| ALL_TASKS_COMPLETE | Proceed to step 5 |
| Some tasks skipped | Proceed to step 5 (report skips) |
| Agent returns error | Read logs, proceed to step 5 (report failure) |
| Timeout | Read partial results, proceed to step 5 |
| Simple task fails inline | Fix, retry once. If still fails, re-classify as complex for run-task.sh |

## Rules

- NEVER use `cd` — run-task.sh takes the repo path as first argument
- NEVER call `bash run-task.sh` directly from the interactive session — always use background Agent + `env -u CLAUDECODE`
- Simple tasks execute inline — the outer agent does the work directly, no process spawning
- Complex tasks always go through run-task.sh for isolation and timeout protection
- Default to complex when uncertain — the cost of unnecessary isolation is low, the cost of a crashed inline task is high
- Sub-agents spawned by run-task.sh are kernel-governed (session-start, anchor, complete)
- Always pass `backlog_path` as 4th arg to run-task.sh for automatic move-to-done
