---
name: on-failure
type: checkpoint
parent: game-engine
---

# On Failure — Diagnosis Tree

## Phase 1 Failures (Discovery + GDD)

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| User disengaged | Too many questions, too fast | Slow down, offer defaults, ask fewer questions per section |
| Section too vague | Skipped discovery questions | Re-read gdd-reference for that section, ask targeted follow-ups |
| Missing REQ IDs | Generated section without them | Scan section for testable behaviors, assign REQ IDs |
| Partial file left | Session ended mid-section | Resume from partial: read discovery progress, continue from last question |
| Profile not saving | State file write error | Check permissions on `.claude/state/`, retry save |

## Phase Transition Failures

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Gate fails on section count | Sections skipped during walkthrough | Compare applicable list vs completed, resume Step 3 for missing |
| Gate fails on partials | User paused mid-section | Complete partial sections or remove from applicable list (with user approval) |
| Gate fails on REQ IDs | Section generated pre-REQ convention | Add REQ IDs to section, resave |

## Phase 3 Failures (Build)

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Test fails for REQ | Implementation doesn't match GDD spec | Read the GDD section for exact formula/behavior, fix code to match |
| Import error | Dependency system not built yet | Check backlog order, build prerequisite system first |
| Coverage script fails | Orphan REQ or orphan test | Map orphans back to GDD sections, write missing tests or remove stale ones |
| External dep not found | Package not installed at scaffold | Read external-deps GDD section, install missing package |
| Hardcoded values | Balance lever in source code | Extract to config file, update code to read from config |

## Recovery Protocol

1. **Diagnose** — match symptom to table above
2. **Fix** — apply the specific fix
3. **Verify** — re-run the failing check
4. **Learn** — if fix reveals a pattern gap, invoke `/kernel/learn`
5. **Resume** — continue from the step that failed
