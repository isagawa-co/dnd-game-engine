# Website Cloner — Clone Any Website via Playwright MCP

**Skill Type:** Extraction + Generation
**Entry Point:** `/clone <url> [output-dir]`
**MCP Required:** Playwright MCP (`@playwright/mcp` in `.mcp.json`)

---

## Usage

```
/clone https://example.com
/clone https://example.com my-clone/
```

- **URL** (required): The page to clone
- **Output directory** (optional): Defaults to `cloned-sites/[domain]/`

---

## Pipeline

| Step | Action | Reference |
|------|--------|-----------|
| 1 | Navigate & screenshot | `references/extraction.md` — Section: Navigate |
| 2 | Extract page data | `references/extraction.md` — Section: Extract |
| 3 | Generate HTML/CSS | `references/generation.md` — Section: Generate |
| 4 | Download assets | `references/generation.md` — Section: Assets |
| 5 | Assemble output | `references/generation.md` — Section: Output |
| 6 | Visual QA | `references/generation.md` — Section: QA |

---

## Output Structure

```
[output-dir]/
  index.html          ← Clean semantic HTML
  styles.css          ← Organized CSS with variables
  assets/
    images/           ← Downloaded images
    fonts/            ← Local font files (if applicable)
```

---

## Principles

1. **Clean semantic HTML.** Use `<header>`, `<nav>`, `<main>`, `<section>`, `<footer>` — not nested `<div>` soup. Reflect the page's actual structure.

2. **Actual fonts and colors.** Extract real font families, weights, and color values via `getComputedStyle()`. Never guess or approximate.

3. **Responsive breakpoints.** Extract media queries from the original site. Include them in `styles.css` at the same breakpoints.

4. **Self-contained output.** The output folder must work when opened directly in a browser. No build step, no dependencies, no CDN links that might break.

5. **No inline styles.** All styling goes in `styles.css`. HTML elements reference CSS classes.

6. **Exact values, not estimates.** Use `getComputedStyle()` for every CSS property. `rgb(31, 41, 55)` not "dark gray". `18px` not "medium text".

7. **Extract all states.** If a component has hover, active, focus, or scroll-triggered states — extract before AND after styles.

8. **Download assets.** Images, SVGs, and fonts get downloaded to the `assets/` folder. Update `src` and `url()` references to point to local copies.

9. **Detect non-DOM rendering.** After typography extraction, run the sanity check (Step 4f). If all values are identical defaults, the site likely uses canvas, SVG text, or deferred hydration — apply fallback strategies before accepting values.

---

## File Index

| File | Purpose |
|------|---------|
| `SKILL.md` | This file — identity, pipeline, principles |
| `references/extraction.md` | How to extract page data via Playwright MCP |
| `references/generation.md` | How to generate HTML/CSS from extracted data |
| `research/repo-analysis.md` | Open source repo research findings |
| `research/gap-analysis.md` | Capability comparison with our Playwright MCP |
| `research/decision-matrix.md` | Scoring matrix for approach selection |
| `research/decision.md` | Final decision: Option B (thin wrapper) |
