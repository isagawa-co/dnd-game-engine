# Verify All Gates

## Context
Run all gate checks to verify rest loop is complete and correct.

## Type
TEST

## Execution
inline

## Dependencies
- 001-006

## Requirements
- Run all BUILD gates (file existence)
- Run all FUNC gates (function behavior)
- Run all TEST gates (pytest passes)
- Verify 100% gate pass rate

## Acceptance Criteria
- [ ] All BUILD gates pass
- [ ] All FUNC gates pass
- [ ] All TEST gates pass
- [ ] gate-contract.md updated with pass status

## Gates Satisfied
- All gates

## Completion Signal
When ALL acceptance criteria are met, invoke `/kernel/complete`.
