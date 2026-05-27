# Decision: Website Cloner Skill Approach

## Decision: Option B — Thin Wrapper (Build Our Own Skill Using Extraction Knowledge)

## Reasoning

1. **Zero capability gap.** Every MCP tool the open source repo uses maps directly to our existing Playwright MCP. The gap analysis (gap-analysis.md) confirmed no missing tools.

2. **The open source repo IS a prompt.** JCodesMore's entire skill is a single SKILL.md file — zero executable code. The value is in the extraction knowledge (what JS to run, what to check for), not in any library or utility.

3. **Different output target.** The open source repo generates Next.js + Tailwind. We want clean HTML + CSS — simpler, more portable, no build toolchain required. Forking would mean stripping out all the React/Next.js specifics.

4. **No dependency risk.** Option B is self-contained. No upstream repo to track, no breaking changes to absorb, no license concerns.

5. **Borrow the knowledge, not the code.** The extraction techniques (getComputedStyle, font detection, scroll library detection, layered image discovery) are universal. We encode these as reference files in our skill.

## Implementation Plan (Tasks 006-009)

### Task 006: SKILL.md
- Skill identity and pipeline overview
- Step table: navigate -> extract -> generate -> output
- File index pointing to references
- Principles: clean HTML, actual fonts, responsive, self-contained

### Task 007: references/extraction.md
- Step-by-step Playwright MCP calls for extraction
- JavaScript snippets for `browser_evaluate`:
  - Computed styles extraction
  - Font discovery (document.fonts, @font-face, Google Fonts links)
  - CSS custom properties
  - Media query breakpoints
  - Image/SVG extraction
  - Layout detection (flex/grid)
- Edge case handling: lazy images, CSS-in-JS, web fonts

### Task 008: references/generation.md
- How to convert extracted data into clean HTML + CSS
- CSS organization: variables, components, responsive
- Font handling: Google Fonts links or @font-face
- Image handling: download to assets/
- Output structure: index.html + styles.css + assets/
- Quality rules: no inline styles, semantic HTML

### Task 009: .claude/commands/clone.md
- Thin command wrapper: parse args, invoke skill
- Usage: `/clone <url> [output-dir]`
- Default output dir: `cloned-sites/[domain]/`
