# Step 3: Convention Check

Verify structural conventions against sibling repos before resolving a template or decomposing.

## When This Step Applies

**MANDATORY** for any BUILD or REFACTOR that targets a repo with siblings — repos in the same org or repos that share an architecture pattern. This includes:
- QA platforms (`isagawa-qa/`)
- Domain specs (`isagawa-co/*-spec`)
- Any repo that follows a shared structural pattern with other repos
- Any new repo being created from a template

**Skip** only if the goal is a truly standalone deliverable with no sibling repos to reference (e.g., a one-off script, a research doc, or a first-of-its-kind repo).

## Why This Step Exists

The agent repeatedly inherited wrong conventions from a single repo without verifying against siblings:
- One repo had test infrastructure in the wrong directory — 3 sibling repos had it right
- The agent assumed the target repo was correct and built a path-mapping from it
- 30 task files would have been written with wrong paths before the user caught it

**One repo is a data point. Multiple repos are a convention.**

## Process

1. **Identify sibling repos:**
   - Determine which org(s) the target belongs to
   - List repos in those orgs: `gh repo list [ORG]`
   - Also check related orgs (e.g., if target is in `isagawa-qa/`, also check `isagawa-co/` for domain specs that follow the same pattern)
   - Select at least 2 siblings that share the same structural pattern
   - Prefer repos that are production-validated (have completed work, have test results)

2. **Read directory structures:**
   - For each sibling: `gh api repos/ORG/REPO/git/trees/HEAD?recursive=1 --jq '.tree[].path'`
   - Identify the structural patterns relevant to the domain:
     - For code repos: source layout, test layout, config locations, build artifacts
     - For spec repos: skill structure, reference layout, command registration
     - For any repo: where docs live, where data/fixtures live, what the entry points are

3. **Compare conventions across siblings:**

   | Convention | Sibling 1 | Sibling 2 | Target Repo | Consistent? |
   |------------|-----------|-----------|-------------|-------------|
   | [convention 1] | ? | ? | ? | ✓/✗ |
   | [convention 2] | ? | ? | ? | ✓/✗ |
   | [convention 3] | ? | ? | ? | ✓/✗ |

   The specific conventions to check depend on the domain — there is no fixed list. The agent must identify what the structural patterns ARE by reading the siblings, then check whether the target follows them.

4. **Determine the correct convention:**
   - **Majority rules** — if most siblings follow a pattern, that's the convention
   - If the target repo deviates, flag it as a structural correction to include in the build/refactor
   - If building NEW, adopt the majority convention — do not copy from the outlier

5. **Document findings:**
   - Write `_context/convention-check.json` with:
     ```json
     {
       "siblings_checked": ["repo-1", "repo-2", "repo-3"],
       "orgs_checked": ["org-1", "org-2"],
       "conventions": {
         "[convention_name]": "[established pattern]",
         "[convention_name]": "[established pattern]"
       },
       "target_deviations": [
         "[what the target does differently]"
       ],
       "correction_required": true
     }
     ```

## Output

```
CONVENTION CHECK

Siblings checked: [list]
Orgs checked: [list]
Conventions verified: N
Target deviations: M

[If deviations found:]
Structural corrections required:
- [deviation 1] → [correction]
- [deviation 2] → [correction]

_context/convention-check.json written

Proceeding to resolve template.
```

## Rules

- NEVER skip this step for repos with siblings — it is the only thing preventing convention drift
- NEVER treat a single repo's structure as authoritative without cross-referencing siblings
- If only one sibling exists, read that sibling's documentation (SKILL.md, FRAMEWORK.md, README) for the canonical convention
- Deviations in the target repo become structural correction tasks in the decomposition — they are not ignored
- This step replaces assumptions with evidence
- The conventions to check are domain-specific — don't hardcode a fixed checklist. Discover what the patterns are by reading the siblings.
