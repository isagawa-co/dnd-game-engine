# Character Pool — Shared Character Registry

## Status
Done

## Priority
High — Characters are currently campaign-local (saved in `campaigns/<id>/party.json`). Need shared pool so characters can be reused across campaigns.

## Summary
Create a shared character registry at `characters/` (repo root). Each character is stored as an individual JSON file (`characters/<character-id>.json`). Campaigns reference characters by ID instead of embedding full entities. Update the character-creation-loop skill, character skill contracts, and campaign loader to support the pool pattern.

## Design Documents

| Document | Purpose |
|----------|---------|
| [[025-domain-build-character-pool/character-pool-contract]] | JSON schema for character pool entries and campaign references |
| [[025-domain-build-character-pool/skill-updates]] | Changes to character-creation-loop Part 5 and character SKILL.md |
| [[025-domain-build-character-pool/campaign-integration]] | How campaigns reference and load characters from pool |

## Requirements
- Create `characters/` directory at repo root
- Define character pool contract (JSON schema for stored characters)
- Each character file: `characters/<character-id>.json` (full Tier 4 entity)
- Campaign `party.json` stores character ID references, not full entities
- Campaign loader resolves character IDs to full entities at load time
- Character-creation-loop Part 5 saves to `characters/` AND updates campaign references
- Characters carry their own history (campaigns played, levels gained, etc.)
- Support "copy on use" — campaign can snapshot a character at join time so leveling in one campaign doesn't affect another
- Validation: character pool entries must pass CHAR-001 through CHAR-008

## References
- Character creation contract: `.claude/skills/character/contracts/character-creation-contract.json`
- Character creation loop: `.claude/skills/character-creation-loop/character-creation-loop.md`
- Character SKILL.md: `.claude/skills/character/SKILL.md`
- Existing fixtures: `.claude/skills/character/fixtures/` (template examples)

## Task Builder Input
- **Deliverable:** Shared character pool system with contract, updated skills, and campaign integration
- **Location:** workspace
- **Scope:** BUILD
- **Constraints:** Depends on 024 (flatten repo) completing first so paths are correct. Must integrate with existing character-creation-loop skill pattern (prescriptive, no Python).
