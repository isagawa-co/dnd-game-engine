# Gate Contract — D&D Item-Use Loop

## BUILD Gates

| Gate | Description | Verification |
|------|-------------|-------------|
| BUILD-01 | item-use-loop-contract.json exists | `os.path.exists(contract_path)` |
| BUILD-02 | item-effect-catalog.json exists | `os.path.exists(catalog_path)` |
| BUILD-03 | attunement-rules.json exists | `os.path.exists(attunement_path)` |
| BUILD-04 | validation-rules.json exists | `os.path.exists(validation_path)` |
| BUILD-05 | SKILL.md exists | `os.path.exists(skill_path)` |

## FUNC Gates

| Gate | Description | Verification |
|------|-------------|-------------|
| FUNC-01 | Contract has valid input/output schemas | `json.loads(contract)` has input_schema and output_schema |
| FUNC-02 | Catalog covers 4 item types | All of potion, equipment, magical_item, consumable present |
| FUNC-03 | Attunement has 4 rules | `len(rules) == 4` |
| FUNC-04 | Validation has 6 rules | `len(rules) == 6` with VAL-001 through VAL-006 |
| FUNC-05 | SKILL.md references all contracts | All 4 contract wikilinks present |

## TEST Gates

| Gate | Description | Verification |
|------|-------------|-------------|
| TEST-01 | Contract tests pass | pytest test_item_use_contract.py — all pass |
| TEST-02 | Effect tests pass | pytest test_item_effects.py — all pass |
| TEST-03 | Validation tests pass | pytest test_item_validation.py — all pass |
| TEST-04 | Integration tests pass | pytest test_item_use_loop.py — all pass |

## Completion Criteria
All BUILD-01 through BUILD-05, FUNC-01 through FUNC-05, and TEST-01 through TEST-04 must pass.
