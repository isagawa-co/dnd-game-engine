# Task 002: Adventure Scene Contract

## Type
BUILD

## Goal
Create `contracts/adventure-scene-contract.json` — the JSON schema for act files.

## Schema
- act_id, chapter, act, title, level_range, location, read_aloud
- encounters array (type, trigger, surprise, enemies, tactics, difficulty, reward_xp)
- transitions object (outcome → next act_id)
- Optional: npcs, loot, skill_checks, traps, secrets, conditions, dm_notes

## Verification
- File exists at `contracts/adventure-scene-contract.json`
- Valid JSON schema
- Matches act file format used in task 004
