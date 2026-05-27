---
step: 5
name: Phase Transition Gate
requires: approved_gdd
produces: gate_pass_or_fail
---

# Step 5: Phase Transition Gate

## Purpose

Structural gate between Phase 1 (design) and Phase 3 (build). Verifies the GDD is structurally complete before any code is generated. This gate is automatic — it fires when `/game-build` is invoked.

## Input

- `docs/game-design/` directory
- State file with GDD completion data
- `gate-contract.md` (TRANS-01 through TRANS-03)

## Actions

1. **Check TRANS-01** — count section files vs applicable sections in state
   - `ls docs/game-design/sections/*.md` (excluding `.partial.md`)
   - Compare count to `gdd_sections_applicable` length
   - FAIL if counts don't match
2. **Check TRANS-02** — verify profile approval
   - Read state file, check `game_profile_approved: true`
   - FAIL if not approved
3. **Check TRANS-03** — no partial files
   - `find docs/game-design/sections/ -name "*.partial.md"`
   - FAIL if any found
4. **Additional checks:**
   - Every section file contains at least one `REQ-` pattern
   - `docs/game-design/profile.md` exists and has genre + platform
   - `docs/game-design/index.md` exists and shows all sections complete

5. **Report result:**
   ```
   PHASE TRANSITION GATE — [PASS/FAIL]

   Sections: M/N complete
   Partial files: 0
   Profile approved: yes
   REQ coverage: all sections have REQ IDs

   [If FAIL: list specific failures and how to fix]
   ```

6. **On PASS** — proceed to Step 6 (decomposition)
7. **On FAIL** — report what's missing, direct user back to `/game-create`

## Output

- Gate result: PASS or FAIL with details
- On PASS: Phase 2+3 proceeds automatically

## Verification

- [ ] All applicable sections have non-partial files
- [ ] Profile is approved in state
- [ ] No `.partial.md` files exist
- [ ] Every section has REQ IDs
- [ ] Gate result is unambiguous PASS or FAIL

## Failure Modes

| Failure | Symptom | Recovery |
|---------|---------|----------|
| Missing sections | Count mismatch | Report which sections are missing, user re-enters /game-create |
| Partial sections remain | `.partial.md` files found | Complete those sections in /game-create |
| Profile not approved | State missing approval flag | Re-run Step 1 profile approval |
