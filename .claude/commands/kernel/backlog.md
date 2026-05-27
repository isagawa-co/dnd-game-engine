# /kernel/backlog

Create a new backlog item in the standard format.

## Usage

```
/kernel/backlog Research AI opportunities for Roberts Hawaii — warm contact with VP of HR
/kernel/backlog Build RAGA eval spec using DeepEval as template
/kernel/backlog Fix safe bash counter skip in master kernel
```

## Instructions

1. **Parse the input:**
   - Extract the core idea
   - Determine the tag: `kernel`, `domain`, `market`, `test`, or new tag if needed
   - Determine the verb: `research`, `build`, `fix`, `test`, `add`, `define`
   - Determine scope: BUILD, RESEARCH, TEST, or REFACTOR

2. **Get next number:**
   - Scan `docs/backlog/*.md` for the highest existing number
   - Next number = highest + 1 (skip numbers in `docs/backlog/done/`)

3. **Record intent:**
   - After determining the backlog number, record the intent for the chain:
     ```bash
     python lib/attestation/intent.py record NNN "the raw argument text" docs/backlog/NNN-tag-verb-object.md
     ```
   - For **new items** (file doesn't exist yet): run this BEFORE writing the file. `record_intent` handles missing `backlog_path` by hashing an empty string for `backlog_hash_after`.
   - For **updates to existing items**: run this AFTER the file is written so `backlog_hash_after` captures the updated content.
   - The intent log is append-only. Each invocation of /kernel/backlog adds one entry.

4. **Assess complexity:**
   - **Simple** — single deliverable, few requirements, fits in one file (<80 lines)
   - **Complex** — multiple components/phases, detailed requirements, would exceed 80 lines

5. **Write the file (simple items):**

   Path: `docs/backlog/NNN-[tag]-[verb]-[object].md`

   Template:

   ```markdown
   # [Title]

   ## Status
   Open

   ## Priority
   [High | Medium | Low] — [one-line reason]

   ## Summary
   [2-3 sentences explaining what this is and why it matters]

   ## Requirements
   - [Key requirement or question 1]
   - [Key requirement or question 2]
   - [Key requirement or question 3]

   ## References
   - [Any relevant links, repos, contacts, backlog items]

   ## Task Builder Input
   - **Deliverable:** [What must exist when done]
   - **Location:** [Where the deliverable lives — see location types below]
   - **Scope:** [BUILD | RESEARCH | TEST | REFACTOR]
   - **Constraints:** [Repos, dependencies, human decisions, blockers]
   ```

6. **Decompose into sub-documents (complex items):**

   When the backlog item is complex (multiple components, phases, or would exceed ~80 lines), decompose it:

   a. **Create a sub-folder:**
      ```
      docs/backlog/NNN-[tag]-[verb]-[object]/
      ```

   b. **Write one sub-document per component/phase/major concern:**
      - Each component that needs to be built or enhanced gets its own file
      - Each phase of delivery gets its own file
      - Cross-cutting design concerns get their own file
      - Name files by what they describe: `source-file-analyzer.md`, `llm-integration.md`, `pattern-agnostic-design.md`

      Common sub-document types:
      - `pipeline.md` — execution architecture / data flow
      - `spec-architecture.md` — file structure, required artifacts
      - `design-decisions.md` — resolved decisions with rationale
      - `design-principles.md` — guiding principles and trade-offs
      - `open-gaps.md` — unresolved questions, blockers
      - `gaps-analysis.md` — identified gaps and risks
      - Component-specific files for each buildable piece

   c. **Each sub-document should include:**
      - Status (NEW / exists — needs enhancement / future)
      - Location (where the code lives or will live)
      - What it does / what it needs
      - Input/output schema if applicable
      - Dependencies on other components
      - Enough detail for task-builder to create granular tasks from it

   d. **Main file becomes an index** with:
      - Status, Priority, Summary (same as simple)
      - **Design Documents table** — wikilinks to each sub-document with purpose
      - Architecture/flow diagram showing how components connect
      - Phases overview (if multi-phase)
      - Requirements (high-level, not duplicating sub-docs)
      - References
      - Task Builder Input

   e. **Design Documents table format:**
      ```markdown
      ## Design Documents

      | Document | Purpose |
      |----------|---------|
      | [[NNN-tag-verb-object/component-name]] | One-line description |
      | [[NNN-tag-verb-object/other-component]] | One-line description |
      ```

7. **Set deliverable location (AUTO-RESOLVE — never ask the user):**

   Every backlog item must specify WHERE the deliverable goes in the `Location` field of Task Builder Input. Three location types with automatic path resolution:

   | Type | Location Field Value | When to use | Example |
   |------|---------------------|-------------|---------|
   | `workspace` | `workspace` or `workspace:[path]` | Feature, fix, or enhancement in this repo | `workspace:.claude/commands/`, `workspace:projects/readmissions/` |
   | `new-repo` | `new-repo:[path]` | Standalone app, library, or spec that gets its own repo | `new-repo:D:\my_ai_projects\fraud-detection-app` |
   | `subproject` | `subproject:[name]` | Multi-file deliverable living under `projects/` in this workspace | `subproject:vietnam-trip`, `subproject:30-day-readmissions` |

   **Auto-resolution rules (MANDATORY — do NOT ask the user for paths):**

   | Deliverable type | Auto-resolved path |
   |-----------------|-------------------|
   | New app, tool, or standalone project | `new-repo:D:\my_ai_projects\[project-name-kebab]` |
   | New domain spec, or testing a domain spec | `new-repo:D:\my_ai_projects\project_test_repos\[project-name-kebab]` |
   | Feature/fix/enhancement to this workspace | `workspace` (or `workspace:[subpath]` if scoped) |
   | Research, notes, or multi-file non-code project | `subproject:[name]` → `projects/[name]/` |

   **How to determine — decision tree:**
   1. Does the deliverable say "spec", "domain spec", "test repo", or "testing platform"? → `new-repo:D:\my_ai_projects\project_test_repos\[name]`
   2. Does it say "app", "repo", "tool", "pipeline", "platform", or "library"? → `new-repo:D:\my_ai_projects\[name]`
   3. Is it a change to existing files in this workspace (commands, protocols, skills, fixes)? → `workspace`
   4. Is it research, notes, or a multi-file deliverable that belongs alongside other projects? → `subproject:[name]`
   5. Fallback: `workspace`

8. **Report:**
   ```
   BACKLOG ITEM CREATED

   File: docs/backlog/NNN-[tag]-[verb]-[object].md
   Title: [title]
   Priority: [priority]
   Scope: [scope]
   Structure: [simple | decomposed (N sub-documents)]

   Ready for /kernel/task-builder.
   ```

## Rules

- Ask the user for priority if not obvious from context
- If the user provides detailed requirements, include them all — don't summarize away detail
- The Task Builder Input section is MANDATORY — every backlog item must be task-builder-ready
- Use the naming convention: `NNN-[tag]-verb-object.md`
- **Decompose when complex** — if the item has multiple components, phases, or detailed requirements that would make the main file unwieldy (>80 lines), break it into sub-documents. The main file should be an index, not a wall of text.
- Sub-documents should be granular enough for task-builder to create one or more tasks per sub-document
- Wikilinks use the format `[[NNN-tag-verb-object/document-name]]` (no `.md` extension)
- Companion folder name MUST match the backlog filename (minus `.md`)
- Task builder reads the Design Documents table to discover reference material during decomposition
