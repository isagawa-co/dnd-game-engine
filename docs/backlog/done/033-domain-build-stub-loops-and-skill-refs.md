# Build Stub Loops and Update Skill Contract References

## Status
Done

## Priority
High — 4 encounter types (social, merchant, travel, item-use) are stubs in the scene dispatcher, forcing the narration fallback to handle them ad-hoc. Scene and Campaign SKILL.md files don't reference their imported contracts, so the agent may not discover them.

## Summary
Build the 4 remaining stub loops (social, merchant, travel, item-use) as proper SKILL.md files with contracts, following the same pattern as combat/challenge/rest. Update Scene SKILL.md and Campaign SKILL.md to reference all their contracts in their Contracts tables.

## Design Documents

| Document | Purpose |
|----------|---------|
| [[033-domain-build-stub-loops-and-skill-refs/social-loop]] | Social encounter loop — NPC conversations, persuasion, deception, intimidation |
| [[033-domain-build-stub-loops-and-skill-refs/merchant-loop]] | Merchant loop — buying, selling, bartering with price negotiation |
| [[033-domain-build-stub-loops-and-skill-refs/travel-loop]] | Travel loop — overland movement, random encounters, navigation |
| [[033-domain-build-stub-loops-and-skill-refs/item-use-loop]] | Item-use loop — potions, scrolls, magic items outside combat |
| [[033-domain-build-stub-loops-and-skill-refs/scene-skill-update]] | Update Scene SKILL.md contracts table |
| [[033-domain-build-stub-loops-and-skill-refs/campaign-skill-update]] | Update Campaign SKILL.md contracts table |

## Requirements
- Each new loop follows the SKILL.md pattern: Identity table, Vocabulary, Contracts, Resolution Flow, Agent Execution, Integration
- Each loop gets at least an action contract and outcome contract
- Scene SKILL.md Contracts table must list all 4 scene contracts
- Campaign SKILL.md must add a Contracts table listing all 6 campaign contracts
- All loops integrate with action-prompt skill for user choices
- All loops return outcome dicts to scene loop for state mutation

## References
- Existing loop patterns: `.claude/skills/combat/SKILL.md`, `.claude/skills/challenge/SKILL.md`, `.claude/skills/rest/SKILL.md`
- Scene skill: `.claude/skills/scene/SKILL.md`
- Campaign skill: `.claude/skills/campaign/SKILL.md`
- Scene contracts: `.claude/skills/scene/contracts/`
- Campaign contracts: `.claude/skills/campaign/contracts/`
- State evaluation: `contracts/state-evaluation-contract.json`

## Task Builder Input
- **Deliverable:** 4 new loop SKILL.md files with contracts + 2 updated SKILL.md files
- **Location:** workspace:.claude/skills/
- **Scope:** BUILD
- **Constraints:** Must follow existing SKILL.md patterns exactly. Must not modify existing combat/challenge/rest loops. Additive only.
