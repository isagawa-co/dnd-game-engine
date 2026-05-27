# Step 7: Plan Review

Spawn a sub-agent to audit the decomposition plan against the convention check and path mapping before writing task files.

## Pipeline Mode — Skip Check

If `pipeline_mode.skip_plan_review` is `true` in `.claude/state/session_state.json`, **skip this entire step** and proceed directly to step 8 (write tasks).

This flag is set by `/kernel/execute-pipeline` when running the full autonomous pipeline (backlog → task-builder → run-task.sh). The pipeline skips plan review because execution is fully autonomous with no user pause points.

**Check:**
1. Read `.claude/state/session_state.json`
2. If `pipeline_mode` exists AND `pipeline_mode.skip_plan_review` is `true`:
   - Log: `"Plan review skipped (pipeline_mode.skip_plan_review = true)"`
   - Proceed to step 8
3. Otherwise: continue with plan review below

## When This Step Applies

**ALWAYS.** This is not optional. Every task-builder run validates the plan here before committing to task files.

## Why This Step Exists

The agent repeatedly built incorrect plans that produced wasted work:
- Wrong directory conventions propagated into 30+ task files before the user caught it
- Structural patterns misunderstood, leading to incorrect decomposition
- Existing patterns not recognized, leading to unnecessary new abstractions

Writing task files is expensive — each file becomes a commitment the cycling engine executes. Catching errors here costs one spawned agent. Catching errors during execution costs a full cycle.

## Process

1. **Spawn a review agent** with this prompt:

   ```
   Review the task-builder plan for [project-name].

   Read these files:
   - tasks/[project-name]/_context/path-mapping.json
   - tasks/[project-name]/_context/convention-check.json (if exists)
   - tasks/[project-name]/_context/template-file-map.json (if exists)
   - tasks/[project-name]/gate-contract.md

   Then verify:

   1. PATH CONSISTENCY: Every file path in the gate contract traces back to
      path-mapping.json. No invented paths. No paths that exist in neither
      new_files nor modified_files.

   2. CONVENTION COMPLIANCE: If convention-check.json exists, every new file
      path follows the established conventions. No paths that match flagged
      deviations.

   3. GATE COVERAGE: Every new_file and modified_file in path-mapping.json
      has at least one corresponding gate in gate-contract.md.

   4. STRUCTURAL INTEGRITY: The decomposition respects the target repo's
      architecture. New files follow the same patterns as existing files.
      No architectural violations (e.g., putting implementation in the wrong
      layer, mixing concerns across directories).

   5. TEST COMPLETENESS: L1 (exists), L2 (runs), and L3 (production) gates
      all present for key deliverables.

   Report:
   - PASS: [check] — [evidence]
   - FAIL: [check] — [what's wrong] — [how to fix]

   Return the full report.
   ```

2. **Process the agent's report:**
   - If all checks PASS → proceed to step 8
   - If any check FAILS → fix the issue (update path-mapping, gate contract, or decomposition), then re-run the review agent
   - Maximum 2 review cycles — if still failing after 2 fixes, flag to user

3. **Log the review result:**
   - Write `_context/plan-review.json` with:
     ```json
     {
       "reviewed": true,
       "review_cycles": 1,
       "checks_passed": ["path_consistency", "convention_compliance", "gate_coverage", "structural_integrity", "test_completeness"],
       "checks_failed": [],
       "fixes_applied": []
     }
     ```

## Output

```
PLAN REVIEW — [project name]

Agent review: PASS (N/N checks passed)
Review cycles: 1
Fixes applied: 0

_context/plan-review.json written

Proceeding to write tasks.
```

Or if fixes were needed:

```
PLAN REVIEW — [project name]

Agent review: PASS after fixes (N/N checks passed)
Review cycles: 2
Fixes applied:
- [fix 1]
- [fix 2]

_context/plan-review.json written

Proceeding to write tasks.
```

## Rules

- This step is autonomous — no user interaction needed
- The review agent is read-only — it reports findings, it does not modify files
- The main agent applies fixes based on the report, then re-spawns the reviewer if needed
- Maximum 2 review cycles — if the plan can't pass after 2 fixes, something is fundamentally wrong and the user should be consulted
- The review agent checks the PLAN, not the code — code review happens in step 10 (structural audit)
- The checks are domain-agnostic — they work for any repo type, not just QA platforms
