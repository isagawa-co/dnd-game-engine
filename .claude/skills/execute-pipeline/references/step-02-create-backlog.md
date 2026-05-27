# Step 2: Create Backlog Item

Create a backlog item from natural language input. **SKIP if step 1 set `input_mode: existing_backlog`.**

## Skip Check

1. Read `pipeline_state.input_mode` from `session_state.json`
2. If `existing_backlog` → skip this step, proceed to step 3
3. If `natural_language` → continue below

## Process

1. **Invoke `/kernel/backlog` inline** with `pipeline_state.raw_input` as the argument
   - The backlog command parses the input, determines tag/verb/priority/scope
   - It writes the backlog file and reports the path

2. **Capture the backlog file path:**
   - Read the backlog command's output for the file path
   - Update `pipeline_state.backlog_path` in `session_state.json`

3. **All user context passes through verbatim:**
   - Do NOT summarize, rephrase, or drop detail from the user's input
   - The backlog command's Task Builder Input section is what task-builder will read

## Output

```
PIPELINE — BACKLOG CREATED

File: [backlog file path]
Title: [title]
Scope: [scope]

Proceeding to step 3.
```

Or if skipped:

```
PIPELINE — BACKLOG EXISTS (skipping step 2)

File: [pipeline_state.backlog_path]

Proceeding to step 3.
```

## Rules

- This step is a thin wrapper around `/kernel/backlog` — don't duplicate its logic
- The backlog command handles all formatting, numbering, and template compliance
- Only add value: capture the file path and update pipeline state
