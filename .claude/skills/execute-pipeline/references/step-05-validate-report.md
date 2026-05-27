# Step 5: Validate + Report

Read execution results and produce the final pipeline report. Clean up pipeline state.

## Process

1. **Read execution results from pipeline state:**
   - `pipeline_state.execution_exit_code`
   - `pipeline_state.completed_count`
   - `pipeline_state.skipped_count`
   - `pipeline_state.log_path`

2. **Read workflow state for details:**
   - Read `.claude/state/sr_dev_workflow.json` (or current domain workflow)
   - Get `completed_tasks` and `skipped_tasks` arrays
   - Count totals

3. **Read validation report if exists:**
   - Check for `tasks/[folder]/_test/validation-report.json`
   - If exists, read gate results (passed, failed, skipped)

4. **Run attestation (after validation, non-blocking):**

   After reading execution results and validation report, run attestation to produce a cryptographic receipt of the pipeline output:

   ```bash
   python lib/attestation/attest.py <backlog_path> <task_folder>
   ```

   - `<backlog_path>` — the backlog file path from `pipeline_state.backlog_path`
   - `<task_folder>` — the task folder path from `pipeline_state.task_folder`

   **Attestation is evidence, not a gate.** If attestation succeeds, capture the Rekor entry URL for the report. If attestation fails, log a warning and continue — do not fail the pipeline.

   Update `session_state.json` (merge) with attestation result:
   ```json
   {
     "last_attestation": {
       "timestamp": "...",
       "backlog": "<backlog_path>",
       "task_folder": "<task_folder>",
       "status": "success | failed",
       "rekor_url": "<url or null>"
     }
   }
   ```

5. **Update live feed (after attestation):**

   After attestation completes (success or fail), regenerate the portfolio feed data so the new pipeline appears on the live site:

   ```bash
   python D:/my_ai_projects/isagawa-co.github.io/generate-feed.py
   ```

   Then commit the updated data files:

   ```bash
   git -C D:/my_ai_projects/isagawa-co.github.io add feed-data.json feed-count.txt
   git -C D:/my_ai_projects/isagawa-co.github.io commit -m "data: update feed (N entries)"
   ```

   **Feed update is non-blocking.** If it fails (script missing, repo not checked out, etc.), log a warning and continue — do not fail the pipeline.

6. **Produce final report:**

   ```
   PIPELINE COMPLETE

   Backlog: [backlog file path]
   Tasks: [folder] ([total] total, [completed] completed, [skipped] skipped)
   Execution: [PASS | PARTIAL | FAIL]
   Exit code: [0 | non-zero]

   Completed tasks:
   - [task 1]
   - [task 2]
   - ...

   [If skipped tasks:]
   Skipped tasks:
   - [task] — skipped after 3 attempts

   [If validation report:]
   Gates: [passed]/[total] passed

   Attestation: [SIGNED — rekor_url | FAILED — reason | SKIPPED]

   Log: [log path]
   ```

7. **Move backlog to done (on PASS only):**

   If overall result is PASS (all tasks completed, exit 0):
   - Move the backlog `.md` file from `docs/backlog/NNN-*.md` to `docs/backlog/done/NNN-*.md`
   - **Also move the companion folder** if one exists (e.g., `docs/backlog/NNN-tag-verb-object/` → `docs/backlog/done/NNN-tag-verb-object/`)
   - Create `docs/backlog/done/` if it doesn't exist
   - Example:
     ```bash
     mv docs/backlog/037-kernel-fix-anchor-integrity.md docs/backlog/done/
     # If companion folder exists:
     mv docs/backlog/037-kernel-fix-anchor-integrity/ docs/backlog/done/
     ```
   - The companion folder has the same name as the `.md` file minus the extension — always check for it

   If PARTIAL or FAIL, leave the backlog in place — it's not done yet.

8. **Move task folder to completed (on PASS only):**

   If overall result is PASS:
   - Move the task folder from `tasks/[folder]/` to `tasks/completed/[folder]/`
   - Create `tasks/completed/` if it doesn't exist
   - Example: `mv tasks/anchor-integrity/ tasks/completed/anchor-integrity/`

   If PARTIAL or FAIL, leave the task folder in place — it may need re-execution.

   Note: The audit-workflow skill already excludes `tasks/completed/` from scans.

9. **Clean up pipeline state:**

   Remove `pipeline_state` and `pipeline_mode` from `session_state.json`:
   ```json
   {
     "pipeline_state": null,
     "pipeline_mode": null
   }
   ```

10. **Determine overall result:**

   | Condition | Result |
   |-----------|--------|
   | All tasks completed, exit code 0 | PASS |
   | Some tasks skipped, exit code 0 | PARTIAL |
   | Exit code non-zero | FAIL |
   | No tasks completed | FAIL |

## Rules

- Always produce a report, even on failure — the user needs to know what happened
- Always clean up pipeline state — don't leave stale state for the next session
- If the validation report has failed gates, list them explicitly
- The report is the last output of the pipeline — nothing follows it
