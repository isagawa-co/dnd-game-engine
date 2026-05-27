# Framework Architecture

<!-- Seeded: expert knowledge for game-engine spec family structure -->

## Two-Tier Spec Family

The game-engine spec is organized by **stack, not genre**:

- `_shared/` — OPERATE spec containing game design knowledge (GDD template, reference implementation, discovery questions, genre mapping). Genre-agnostic.
- `platform-*/` — BUILD specs containing stack-specific code generation (Python/Pygame, Godot, Phaser, LOVE). One per supported stack.

Genre differences are handled by discovery (which GDD sections apply), not by different spec files. A platformer and a 4X game use the same `_shared/` spec — discovery determines which of the 20 sections are relevant.

## Three-Phase Pipeline

```
Phase 1: /game-create  →  Phase 2: auto-decompose  →  Phase 3: /game-build
(HITL, collaborative)     (mechanical, no HITL)        (autonomous, execute-pipeline)
```

- Phase 1 does the hard thinking with the user. Every design decision is explicit.
- Phase 2 is mechanical. If the GDD is granular enough, decomposition writes itself.
- Phase 3 is autonomous. The agent builds, tests, and verifies against REQ IDs.

## GDD-Driven Development

The GDD is the single source of truth:
1. Every testable behavior has a REQ ID in the GDD
2. Every REQ ID maps to a gate contract row
3. Every gate contract row maps to a test function
4. Coverage script validates bidirectional traceability (no orphans)

If a developer can't implement from the GDD without asking a clarifying question, the GDD section needs more discovery.

## Source

Architecture decisions from backlog 007: spec-architecture.md, pipeline.md, design-decisions.md
