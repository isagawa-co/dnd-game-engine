# Merchant Loop — Gate Contract

## Gates

| Gate ID | Description | Method | Check |
|---------|-------------|--------|-------|
| BUILD-01 | Transaction contract exists | file_exists | `.claude/skills/merchant/contracts/merchant-loop-contract.json` |
| BUILD-02 | Shop inventory contract exists | file_exists | `.claude/skills/merchant/contracts/shop-inventory-contract.json` |
| BUILD-03 | Negotiation contract exists | file_exists | `.claude/skills/merchant/contracts/negotiation-contract.json` |
| BUILD-04 | Merchant SKILL.md exists | file_exists | `.claude/skills/merchant/SKILL.md` |
| TEST-01 | All contracts valid JSON | run_code | `python3 -c "import json; [json.load(open(f'.claude/skills/merchant/contracts/{c}')) for c in ['merchant-loop-contract.json','shop-inventory-contract.json','negotiation-contract.json']]"` |
