# Game Engine — Domain Protocol

<!-- Protocol = Index. Points to files, never duplicates content. -->
<!-- Re-read on every /kernel/anchor. -->

## Domain Identity

| Key | Value |
|-----|-------|
| Domain | game-engine |
| Type | prescriptive |
| Version | 1.0 |

## Skill Files

| File | Purpose |
|------|---------|
| `.claude/skills/game-engine/SKILL.md` | Identity, vocabulary, critical rules, communication guidelines |
| `.claude/skills/game-engine/workflow.md` | Data flow, step index, state persistence, resume flow |
| `.claude/skills/game-engine/gate-contract.md` | GDD quality gates, phase transition gate, build gates, REQ coverage gates |

## Step Files

| Step | File | Action |
|------|------|--------|
| 1 | `.claude/skills/game-engine/steps/step-01.md` | Initial Discovery — genre, scope, platform, art style |
| 2 | `.claude/skills/game-engine/steps/step-02.md` | Genre Section Selection — which GDD sections apply |
| 3 | `.claude/skills/game-engine/steps/step-03.md` | GDD Section Walkthrough — per-section discovery + generation |
| 4 | `.claude/skills/game-engine/steps/step-04.md` | GDD Review — completeness check, user approval |
| 5 | `.claude/skills/game-engine/steps/step-05.md` | Phase Transition Gate — structural gate before build |
| 6 | `.claude/skills/game-engine/steps/step-06.md` | Decompose GDD — systems to ordered backlog items |
| 7 | `.claude/skills/game-engine/steps/step-07.md` | Execute Build Pipeline — autonomous build |
| — | `.claude/skills/game-engine/steps/on-failure.md` | Failure diagnosis tree |
| — | `.claude/skills/game-engine/steps/pre-build.md` | Readiness checkpoint before Phase 2+3 |

## Reference Files

| File | Purpose |
|------|---------|
| `.claude/skills/game-engine/references/gdd-template.md` | 20-section GDD template with genre mapping |
| `.claude/skills/game-engine/references/genre-mapping.md` | Section relevance matrix by genre |
| `.claude/skills/game-engine/references/discovery-questions.md` | Per-section question sets for Phase 1 |

## Commands

| Command | File | Purpose |
|---------|------|---------|
| `/game-create` | `.claude/commands/game-create.md` | Phase 1: Guided GDD creation |
| `/game-build` | `.claude/commands/game-build.md` | Phase 2+3: Decompose + build |

## Lessons Index

| File | Purpose |
|------|---------|
| `.claude/lessons/lessons.md` | Master index — points to topic folders |
| `.claude/lessons/framework/architecture.md` | Two-tier spec family, phase pipeline |
| `.claude/lessons/game/gdd-granularity.md` | GDD sections must be implementer-ready |
| `.claude/lessons/game/discovery-patience.md` | One question at a time |
| `.claude/lessons/game/req-traceability.md` | Every REQ needs a test |
| `.claude/lessons/game/external-deps.md` | Identify, acquire, localize |
| `.claude/lessons/game/balance-levers.md` | Tunable values in config |

## Critical Rules (from SKILL.md)

1. GDD before code
2. One question at a time
3. Collaborate, don't interrogate
4. Granularity over speed
5. Save incrementally
6. REQ IDs are mandatory
7. Don't build what you can pull
8. Phase gate is structural
