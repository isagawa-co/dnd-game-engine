---
step: 4
name: GDD Review
requires: completed_gdd_sections
produces: approved_gdd
---

# Step 4: GDD Review

## Purpose

Verify the complete GDD is ready for build. Check that all applicable sections are complete, every section has REQ IDs, no partial files remain, and the user gives final approval. This is the last checkpoint before Phase 2+3.

## Input

- `docs/game-design/index.md` — section completion status
- `docs/game-design/sections/*.md` — all completed sections
- State file with `gdd_sections_applicable` and `gdd_sections_complete`

## Actions

1. **Read index** — load `docs/game-design/index.md`
2. **Compare** applicable vs complete sections:
   - All applicable sections must have corresponding `.md` files (not `.partial.md`)
   - If any missing: report which sections need completion, offer to resume Step 3
3. **Scan each section** for quality:
   - Has REQ IDs? (every section must have at least one)
   - Has data tables/formulas/enumerations where applicable?
   - Has edge cases documented?
4. **Generate completeness report:**
   ```
   GDD REVIEW — [Game Name]

   Total sections: N applicable, M complete
   REQ IDs: K total across all sections
   Sections with issues: [list any]

   Status: READY / NEEDS WORK
   ```
5. **Present to user** — show report, highlight any issues
6. **HITL gate** — user gives final GDD approval or requests revisions
7. **Update state** — set all sections to final status

## Output

- Completeness report presented to user
- User approval recorded
- State updated: GDD approved, ready for Phase 2+3

## Verification

- [ ] All applicable sections exist as non-partial files
- [ ] Every section has at least one REQ ID
- [ ] REQ IDs follow `REQ-SYSTEM-NNN` format consistently
- [ ] No orphan sections (sections not in applicable list)
- [ ] User gave explicit approval
- [ ] `index.md` shows all sections as "complete"

## Failure Modes

| Failure | Symptom | Recovery |
|---------|---------|----------|
| Incomplete sections | `.partial.md` files remain | Resume Step 3 for those sections |
| Missing REQ IDs | Section has no `REQ-` patterns | Scan section for testable behaviors, assign REQ IDs |
| Vague sections | Section lacks data tables | Flag specific deficiencies, re-enter discovery |
| User wants changes | Revision request after review | Return to Step 3 with revision workflow |
