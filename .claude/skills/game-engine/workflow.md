---
name: game-engine-workflow
type: workflow
parent: game-engine
---

# Game Engine — Workflow

## Data Flow

```
Phase 1: /game-create
  User idea
    → [Step 1] Initial Discovery → Game Profile (genre, scope, platform, art)
    → [Step 2] Genre Section Selection → Applicable GDD sections list
    → [Step 3] GDD Section Walkthrough → Completed sections with REQ IDs
    → [Step 4] GDD Review → Approved GDD (all sections final)

Phase 2+3: /game-build
  Approved GDD
    → [Step 5] Phase Transition Gate → Gate pass/fail
    → [Step 6] Decompose GDD → Ordered backlog items (one per system)
    → [Step 7] Execute Build Pipeline → Working game + tests + REQ coverage
```

## Step Index — Phase 1 (/game-create)

| Step | Input | Output | Fail Action |
|------|-------|--------|-------------|
| 1 | User's game idea | `docs/game-design/profile.md` | Offer 2-3 genre/scope options with tradeoffs |
| 2 | Game profile | Applicable sections list in state | Re-read genre-mapping.md, present alternatives |
| 3 | Selected sections + gdd-reference | `docs/game-design/sections/NN-name.md` per section | Read gdd-reference for calibration, ask targeted follow-ups |
| 4 | All completed sections | Approved GDD, index.md updated | Report incomplete/vague sections, resume discovery |

## Step Index — Phases 2+3 (/game-build)

| Step | Input | Output | Fail Action |
|------|-------|--------|-------------|
| 5 | `docs/game-design/` directory | Gate pass or fail report | List missing sections/REQ IDs, re-enter /game-create |
| 6 | Complete GDD | `backlog/NNN-system-name.md` per system | Re-read GDD, identify core system, break dependency cycle |
| 7 | Backlog items + GDD context | Working game code + tests | Read GDD section for exact spec, fix implementation |

## Pre-Step Reads

### Phase 1
| Step | Must Read Before Acting |
|------|------------------------|
| 1 | `references/discovery-questions.md` (initial section), `references/genre-mapping.md` |
| 2 | `references/genre-mapping.md`, `references/gdd-template.md` |
| 3 | `references/gdd-reference/NN-*.md` (matching section), `references/discovery-questions.md` (matching section) |
| 4 | `docs/game-design/index.md`, all `sections/*.md` files |

### Phase 2+3
| Step | Must Read Before Acting |
|------|------------------------|
| 5 | `docs/game-design/index.md`, `gate-contract.md` (phase transition section) |
| 6 | All `docs/game-design/sections/*.md`, `gate-contract.md` (decomposition section) |
| 7 | Current backlog item, relevant GDD section(s) for that system |

## State Persistence

### Phase 1 State
```json
// .claude/state/game_create_state.json
{
  "current_phase": 1,
  "genre": "4x-strategy",
  "platform": "pygame",
  "gdd_sections_applicable": [1, 2, 3, 5, 6, 7, 8, 14, 15, 18, 19, 20],
  "gdd_sections_complete": [1, 2, 3],
  "gdd_sections_in_progress": [5],
  "next_section": 5,
  "discovery_complete": true,
  "game_profile_approved": true,
  "last_session": "2026-04-07",
  "version": 2
}
```

### Phase 2+3 State
```json
// .claude/state/game_build_state.json
{
  "current_phase": 3,
  "gdd_path": "docs/game-design/",
  "systems_identified": ["map", "units", "combat", "ai", "ui"],
  "systems_built": ["map", "units"],
  "current_system": "combat",
  "backlog_items": ["001-map-system.md", "002-unit-system.md", "003-combat-system.md"],
  "last_session": "2026-04-07"
}
```

### Resume Flow
```
User invokes /game-create or /game-build
  → Read state file
  → State exists?
    ├── No → fresh start (discovery or gate check)
    └── Yes → resume
         → Show status: "6 of 19 sections complete. Section 7 in progress."
         → Read partial file if exists (sections/NN-name.partial.md)
         → Resume at last unanswered question
```

## GDD File Structure

```
docs/game-design/
├── index.md                  ← section index + completion status
├── profile.md                ← game profile from discovery
├── sections/
│   ├── 01-game-loop.md       ← completed, approved
│   ├── 02-world-space.md     ← completed, approved
│   ├── 07-combat.partial.md  ← in progress (partial save)
│   └── ...
└── history/
    ├── 03-entities.v1.md     ← prior version
    └── changelog.md          ← revision log
```

## Domain-Specific Rules

1. **Save on complete** — write each GDD section to `sections/` immediately on user approval. Never batch saves.
2. **Save on pause** — if user stops mid-section, save partial progress to `sections/NN-name.partial.md` with discovery progress block.
3. **Version on revise** — before overwriting a completed section, copy to `history/NN-name.vN.md`. Never delete prior versions.
4. **Index always current** — `index.md` reflects real-time status after every section change.
5. **One question at a time** — during discovery, present one focused question per turn with suggestions and tradeoffs.
6. **REQ IDs at generation time** — assign REQ IDs when generating section content, not retroactively. Format: `REQ-SYSTEM-NNN`.
7. **Phase gate before build** — `/game-build` checks all applicable sections complete, all have REQ IDs, profile approved. No exceptions.
8. **Decomposition is automatic** — Phase 2 requires no HITL. If GDD is granular enough, system identification and ordering is mechanical.
9. **GDD context per task** — during Phase 3, each build task receives only its relevant GDD section(s) as context, not the entire GDD.
10. **External deps at scaffold** — acquire packages/MCPs/APIs once at project scaffold, reference locally thereafter.
