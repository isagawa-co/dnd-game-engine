# Task 003: Game Loop Integration

## Type
BUILD

## Goal
Update game-play command and campaign loop skill to load and follow adventure act files.

## Changes
1. `.claude/commands/game-play.md` — add "Load Adventure" step between load campaign and evaluate state
2. `.claude/skills/campaign/SKILL.md` — add anti-drift rule, act file reading, transition logic
3. Campaign state schema — add adventure_id, current_chapter, current_act, current_act_id, chapters_completed

## Anti-Drift Rule
> MANDATORY: Read current act file before narrating. All encounters, NPCs, locations come from the act file. Do not invent outside it.

## Verification
- game-play.md references adventure loading step
- campaign SKILL.md contains anti-drift rule
- State schema documented with new fields
