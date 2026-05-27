# Task 005: Build Game Session SKILL.md

## Action
Write `.claude/skills/game-session/SKILL.md`

## Source
`docs/backlog/019-dnd-build-game-session-command.md`

## Deliverable
SKILL.md file with:
- Identity: game-session command skill
- Vocabulary: campaign, session, checkpoint, content pack, party
- Contract references: links to all 4 contracts (create, load, save, resume)
- Dependencies: state-model (001), content-system (002), configuration (004), entity-system (005), campaign-loop (006)
- Actions: create_campaign, load_campaign, save_session, resume_session
- Result codes table: campaign_created, campaign_loaded, session_saved, session_resumed, state_corrupted, not_found

## Acceptance Criteria
- [ ] File exists at `.claude/skills/game-session/SKILL.md`
- [ ] Identity section with skill name and purpose
- [ ] Vocabulary section with key terms
- [ ] Contract references section with wiki-links to all 4 contracts
- [ ] Dependencies section listing required skills
- [ ] Actions section with all 4 session actions
- [ ] Result codes table matching session-contract.md
