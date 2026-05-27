# Task 005: Campaign Reset

## Type
BUILD

## Goal
Reset campaign-2026-05-27-002 to LMoP Chapter 1 Act I. Remove Forgotten Throne story data.

## Changes
1. `campaign.json` — update adventure_id, campaign_name, party_pcs
2. `campaign_state.json` — reset to session 1, add adventure tracking fields, clear Forgotten Throne data
3. Delete `session-1-intel.json` (Forgotten Throne intel)
4. Keep `party.json` and all character files

## Verification
- campaign.json has adventure_id: "lmop"
- campaign_state.json has current_chapter: 1, current_act: "I"
- session-1-intel.json removed
- party.json unchanged
