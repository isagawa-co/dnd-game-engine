# External Dependencies

<!-- Seeded: expert knowledge for external dependency resolution -->

## The Problem

Building infrastructure that already exists as a package, MCP, or API wastes time and produces worse results. A custom simplex noise implementation will be buggier than the community-maintained one.

## Why It Fails

- Agent defaults to "build everything from scratch"
- No dependency analysis during GDD discovery
- Runtime API calls for static data (fragile, slow)
- External data fetched every run instead of cached locally

## Correct Approach

**Identify → Acquire → Localize.** During Phase 1 discovery, for each system:

1. What **DATA** does this need? → External dataset or invented?
2. What **COMPUTATION** does this need? → Library or custom?
3. What **ASSETS** does this need? → Asset pack or generated?

**Resolution priority (prefer local):**
1. MCP server → pull at scaffold time, save locally
2. Package/library → add to requirements.txt, import
3. API + download → fetch once, cache in `data/`
4. Generate → only if no external source exists

**Key rule:** Code references local files, never remote sources directly. Acquisition happens once during scaffold. No runtime API calls for static data.

**GDD output format:**
```markdown
Source: ESPN API via sports-data MCP
Acquisition: /game-scaffold pulls roster → data/players.json
REQ-DATA-001: Player data loaded from data/players.json (not API)
```

## Source

Design principle from backlog 007: design-principles.md (External Dependency Resolution)
