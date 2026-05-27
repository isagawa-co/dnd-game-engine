# Step 1: Parse Input

Detect whether the user provided an existing backlog item or a natural language goal.

## Process

1. **Read the argument:**
   - The argument is everything after `/kernel/execute-pipeline`

2. **Detect input mode:**

   | Condition | Mode | Action |
   |-----------|------|--------|
   | Argument ends in `.md` AND file exists | `existing_backlog` | Use file directly, skip step 2 |
   | Argument is a number (e.g., `031`) | `existing_backlog` | Glob `docs/backlog/NNN-*.md`, use match, skip step 2 |
   | Anything else | `natural_language` | Pass to step 2 for backlog creation |

3. **For number shorthand:**
   ```bash
   # Resolve "031" to full path
   ls docs/backlog/031-*.md
   ```
   If no match found, treat as natural language (proceed to step 2).

4. **Set pipeline state:**

   Merge into `session_state.json`:
   ```json
   {
     "pipeline_state": {
       "input_mode": "existing_backlog | natural_language",
       "backlog_path": "docs/backlog/NNN-*.md or null",
       "raw_input": "the original argument"
     }
   }
   ```

## Output

```
PIPELINE — INPUT PARSED

Mode: [existing backlog | natural language]
Backlog: [path | "will create in step 2"]
Input: [original argument]

Proceeding to [step 2 | step 3].
```

## Rules

- If the file path exists, use it — don't re-read or validate its format
- Number shorthand resolves via glob — if multiple matches, use the first
- All context from the argument passes through unmodified
