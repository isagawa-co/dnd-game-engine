# Step 3: Run Task-Builder

Invoke task-builder with flags to stop before execution. Plan review runs normally.

## Process

1. **Set pipeline mode flags:**

   Merge into `session_state.json`:
   ```json
   {
     "pipeline_mode": {
       "skip_plan_review": false,
       "no_execute": true
     }
   }
   ```

   These flags tell task-builder:
   - `skip_plan_review` → when true, skip step 7 (plan review); when false, plan review runs normally
   - `no_execute` → stop after step 8 (write tasks), don't start cycling

2. **Invoke `/kernel/task-builder` inline:**

   Pass `pipeline_state.backlog_path` as the argument:
   ```
   /kernel/task-builder [pipeline_state.backlog_path]
   ```

   Task-builder will:
   - Read the backlog file (Type B input — step 1 of task-builder)
   - Research context (step 2)
   - Convention check (step 3, if applicable)
   - Resolve template (step 4, if applicable)
   - Decompose (step 5)
   - Atomize + gate contract (step 6)
   - **Run plan review** (step 7 — presents plan to user for approval)
   - Write task files (step 8)
   - **Stop and return** (step 9 — flag check, sets `pipeline_state.task_folder` and `pipeline_state.task_count`)

3. **Clear pipeline mode flags:**

   After task-builder returns, merge into `session_state.json`:
   ```json
   {
     "pipeline_mode": null
   }
   ```

4. **Verify handoff state:**
   - Confirm `pipeline_state.task_folder` is set (task-builder's step 9 sets this)
   - Confirm `pipeline_state.task_count` is set
   - If either is missing, read the task folder directly and set them

## Output

```
PIPELINE — TASKS CREATED

Backlog: [backlog path]
Task folder: [task folder]
Tasks: [count]

Proceeding to step 4 (execution).
```

## Rules

- Set flags BEFORE invoking task-builder, clear AFTER it returns
- Task-builder runs the full skill except step 9 — don't skip any other steps
- If task-builder fails (no tasks written), stop the pipeline and report the error
- The flag mechanism is the ONLY modification to task-builder — all other behavior is unchanged
