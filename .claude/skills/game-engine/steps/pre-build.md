---
name: pre-build
type: checkpoint
parent: game-engine
---

# Pre-Build Readiness Checkpoint

Run this checklist before entering Phase 3 (`/game-build`).

## Prerequisites

| # | Check | How to Verify | Fix if Missing |
|---|-------|---------------|----------------|
| 1 | GDD profile exists | `test -f docs/game-design/profile.md` | Run `/game-create`, complete Step 1 |
| 2 | Profile has genre + platform | `grep "genre:" docs/game-design/profile.md` | Re-run Step 1 discovery |
| 3 | All applicable sections complete | Count `sections/*.md` == applicable count | Resume Step 3 for missing sections |
| 4 | No partial sections | `ls sections/*.partial.md` returns empty | Complete partial sections |
| 5 | Every section has REQ IDs | `grep -l "REQ-" sections/*.md` count matches | Add REQ IDs to sections missing them |
| 6 | Index is current | `docs/game-design/index.md` shows all complete | Regenerate index |
| 7 | Coverage script exists | `test -f scripts/req-coverage` or equivalent | Generate from gate-contract.md |
| 8 | Platform stack determined | Profile has `platform:` field | Re-run Step 1 platform question |

## Quick Check Command

```bash
echo "=== Pre-Build Check ==="
test -f docs/game-design/profile.md && echo "✓ Profile" || echo "✗ Profile MISSING"
test -f docs/game-design/index.md && echo "✓ Index" || echo "✗ Index MISSING"
ls docs/game-design/sections/*.md 2>/dev/null | wc -l | xargs -I{} echo "  Sections: {}"
ls docs/game-design/sections/*.partial.md 2>/dev/null | wc -l | xargs -I{} echo "  Partials: {}"
grep -rl "REQ-" docs/game-design/sections/ 2>/dev/null | wc -l | xargs -I{} echo "  With REQs: {}"
test -f scripts/req-coverage && echo "✓ Coverage script" || echo "✗ Coverage script MISSING"
```

## If Any Check Fails

Do NOT proceed to `/game-build`. Return to `/game-create` and complete the missing items. The phase transition gate (Step 5) will catch these anyway, but catching them here saves a round trip.
