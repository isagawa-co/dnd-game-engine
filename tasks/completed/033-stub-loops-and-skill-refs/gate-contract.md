# Gate Contract — Stub Loops and Skill Refs

## Gates

| ID | Check | Method | Pass Criteria | Fail Action |
|----|-------|--------|---------------|-------------|
| BUILD-01 | Social SKILL.md exists | file_exists | `test -f .claude/skills/social/SKILL.md` | Create file |
| BUILD-02 | Social action contract exists | file_exists | `test -f .claude/skills/social/contracts/social-action-contract.json` | Create file |
| BUILD-03 | Social outcome contract exists | file_exists | `test -f .claude/skills/social/contracts/social-outcome-contract.json` | Create file |
| BUILD-04 | Merchant SKILL.md exists | file_exists | `test -f .claude/skills/merchant/SKILL.md` | Create file |
| BUILD-05 | Merchant action contract exists | file_exists | `test -f .claude/skills/merchant/contracts/merchant-action-contract.json` | Create file |
| BUILD-06 | Merchant outcome contract exists | file_exists | `test -f .claude/skills/merchant/contracts/merchant-outcome-contract.json` | Create file |
| BUILD-07 | Travel SKILL.md exists | file_exists | `test -f .claude/skills/travel/SKILL.md` | Create file |
| BUILD-08 | Travel action contract exists | file_exists | `test -f .claude/skills/travel/contracts/travel-action-contract.json` | Create file |
| BUILD-09 | Travel outcome contract exists | file_exists | `test -f .claude/skills/travel/contracts/travel-outcome-contract.json` | Create file |
| BUILD-10 | Item-use SKILL.md exists | file_exists | `test -f .claude/skills/item-use/SKILL.md` | Create file |
| BUILD-11 | Item-use action contract exists | file_exists | `test -f .claude/skills/item-use/contracts/item-use-action-contract.json` | Create file |
| BUILD-12 | Item-use outcome contract exists | file_exists | `test -f .claude/skills/item-use/contracts/item-use-outcome-contract.json` | Create file |
| BUILD-13 | Scene SKILL.md has dispatch contract ref | grep | `grep -q 'scene-dispatch-contract' .claude/skills/scene/SKILL.md` | Add reference |
| BUILD-14 | Scene SKILL.md has encounter-types ref | grep | `grep -q 'scene-encounter-types' .claude/skills/scene/SKILL.md` | Add reference |
| BUILD-15 | Campaign SKILL.md has contracts table | grep | `grep -q 'campaign-loop-contract' .claude/skills/campaign/SKILL.md` | Add table |
| BUILD-16 | Scene SKILL.md shows social as built | grep | `grep -q 'social.*built' .claude/skills/scene/SKILL.md` | Update status |
