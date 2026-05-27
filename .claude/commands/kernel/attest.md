# /kernel/attest

Manually attest any file or directory outside the pipeline.

**Usage:** `/kernel/attest <path> [--dry-run]`

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `path` | Yes | File or directory to attest |
| `--dry-run` | No | Create bundle and compute hashes but skip signing and Rekor |

## Instructions

1. **Parse argument:**
   - Extract the file or directory path from `$ARGUMENTS`
   - Check if `--dry-run` is present in arguments
   - Verify the path exists (file or directory)
   - If path does not exist, report error and stop

2. **Compute SHA-256 of target:**
   - If path is a file: compute SHA-256 of that single file
   - If path is a directory: collect all files recursively, compute SHA-256 of each
   - Report hash summary to user

3. **Run attestation with manual mode:**
   ```bash
   python "D:/my_ai_projects/project_test_repos/sr_dev_workspace/lib/attestation/attest.py" \
     "manual" \
     "<path>" \
     --dry-run  # include only if --dry-run was requested
   ```

   **Note:** When called in manual mode, `backlog_path` is set to the literal string `"manual"` and
   `task_folder` is set to the target path. The orchestrator will create a minimal attestation bundle
   with hashes of the target artifacts. No `pipeline_state` or `task_folder` metadata is needed.

4. **Report results:**
   ```
   ATTESTED: <path>
   Bundle: <bundle file path>
   Artifacts: <count> files hashed
   Rekor: <entry URL or "skipped (dry-run)" or "skipped (unsigned)">
   ```

## Examples

```
# Attest a single file (dry-run)
/kernel/attest lib/attestation/schema.py --dry-run

# Attest an entire directory
/kernel/attest lib/attestation/

# Attest a specific deliverable
/kernel/attest projects/ai-clone-opportunity/decision-framework.md
```

## When to Use

- After completing a deliverable outside the execute-pipeline flow
- To create a tamper-evident record of any artifact
- To verify file integrity before sharing or archiving

## References

- Orchestrator: `lib/attestation/attest.py`
- Schema: `lib/attestation/schema.py`
- Hash collector: `lib/attestation/collect.py`
- Signer: `lib/attestation/sign.py`
- Rekor logger: `lib/attestation/rekor.py`
- Attestation output: `.claude/state/attestations/`
