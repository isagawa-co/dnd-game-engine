# Website Cloner — Open Source Repo Analysis

## Primary Repo: JCodesMore/ai-website-cloner-template

- **URL**: https://github.com/JCodesMore/ai-website-cloner-template
- **Author**: JCodesMore
- **Stars**: ~9,000+ (as of early 2026)
- **Forks**: ~1,200
- **Language**: TypeScript
- **Last Updated**: Active (March/April 2026)
- **License**: Open source template

### What It Claims To Do

Clone any website with one command using AI coding agents. You point it at a URL, run `/clone-website`, and the AI agent inspects the site, extracts design tokens and assets, writes component specs, and dispatches parallel builder agents to reconstruct every section.

### How to Install

Clone the repo template, then use the `/clone-website` slash command inside Claude Code. The skill lives at `.claude/skills/clone-website/SKILL.md` — a single file.

### MCP Used

- **Firecrawl MCP** for web scraping/crawling (primary)
- **Playwright MCP / Chrome MCP** for browser automation (screenshots, `getComputedStyle()` extraction, interaction sweeps)
- Uses browser automation to take screenshots, extract computed styles, and discover interactive behaviors

### Output Format

Generates a Next.js 16 + Tailwind CSS v4 codebase. The output is a full React project, not raw HTML/CSS.

### Pipeline (5 Phases)

1. **Reconnaissance** — Full-page screenshots at desktop (1440px) and mobile (390px), extract fonts/colors/favicons, mandatory interaction sweep (scroll, click, hover), document findings
2. **Foundation Build** — Set up layout.tsx with fonts, populate globals.css with color tokens, extract SVGs, download all assets
3. **Component Specs & Dispatch** — For each section: extract via browser MCP, write spec file with exact computed CSS, dispatch parallel builder agents in git worktrees
4. **Page Assembly** — Import sections, implement page-level layout, scroll containers, sticky positioning
5. **Visual QA** — Side-by-side comparison at 1440px and 390px, test all interactions

### Key Technical Details

- Uses `getComputedStyle()` for exact CSS values (not estimates)
- Multi-state extraction: clicks every tab, captures scroll-driven behaviors
- Layered image detection (background + overlay + z-index)
- Smooth scroll library detection (Lenis, Locomotive Scroll)
- Spec files in `docs/research/components/<ComponentName>.spec.md`
- Parallel builder agents in git worktrees (one per section)
- Complexity assessment: simple sections get one builder, complex sections get split

---

## Secondary Repo: horuz-ai/claude-plugins (website-cloner)

- **URL**: https://github.com/horuz-ai/claude-plugins
- **Author**: horuz-ai
- **Stars**: ~2
- **Language**: Python (87.6%), TypeScript (11.4%)

### Architecture

Four specialized sub-agents:
1. **Screenshotter** — captures full-page, sections, components, hover/interactive states
2. **Extractor** — downloads assets, extracts colors, typography, spacing, animations
3. **Cloner** — generates React + Tailwind + motion code
4. **QA-Reviewer** — pixel-by-pixel comparison, defect classification

### Output

React components with Tailwind CSS and motion animations. Project structure:
```
your-project/
├── public/ (images, videos, icons)
├── app/clone/page.tsx
└── .tasks/clone-{domain}/ (context, screenshots, review notes)
```

### MCP Used

Playwright MCP via `@anthropic-ai/mcp-playwright` configured in `.claude/settings.json`

---

## Other Notable Mentions

- **Linus Ekenstam (X post)** popularized the JCodesMore repo with a viral tweet
- **mcpmarket.com** lists several variants: "Website to Next.js", "Pixel-Perfect Website Cloner"
- **Firecrawl MCP** and **Chrome/Playwright MCP** are the two main browser automation approaches used across these tools

---

## Source Code Analysis: JCodesMore SKILL.md (Deep Dive)

The entire skill is a single SKILL.md file (~400 lines of markdown). There is NO executable code — it is purely an instruction document that Claude Code follows as a prompt. The "source code" IS the prompt.

### MCP Tools Used

The SKILL.md references browser MCP tools for these operations:
1. **browser_navigate** — Navigate to target URL
2. **browser_screenshot** (implied) — Full-page screenshots at 1440px and 390px viewports
3. **browser_evaluate** — Run JavaScript in page context to extract:
   - `getComputedStyle()` on all visible elements
   - Font-face declarations
   - Google Fonts link elements
   - CSS custom properties (variables)
   - Media query breakpoints
   - Image URLs and SVG content
4. **browser_run_code** — Execute more complex extraction scripts
5. **browser_snapshot** — Capture accessibility tree / DOM structure
6. **browser_click** — Click interactive elements to discover states
7. **browser_resize** — Test at different viewport widths (1440, 768, 390)

### Style Extraction Method

The repo uses `getComputedStyle()` exclusively — NOT stylesheet parsing. For each visible element:
```javascript
// Pattern used (conceptual — inline in the prompt, not a script file)
const el = document.querySelector(selector);
const styles = window.getComputedStyle(el);
// Extract: color, backgroundColor, fontSize, fontFamily, padding, margin,
// display, flexDirection, gap, gridTemplateColumns, position, etc.
```

Key insight: It extracts COMPUTED styles (final rendered values), not authored CSS. This means:
- `16px` not `1rem`
- `rgb(0, 0, 0)` not `var(--text-color)`
- Actual pixel values after all cascading

### Font Extraction Method

1. Check `document.fonts` API for loaded fonts
2. Scan for `<link>` elements pointing to Google Fonts / Adobe Fonts CDNs
3. Extract `@font-face` declarations from stylesheets
4. Record font-family, font-weight, font-style for each

### Layout Extraction Method

1. Detect `display: flex` or `display: grid` on containers
2. Extract flex/grid properties: `flex-direction`, `gap`, `grid-template-columns`, `align-items`, `justify-content`
3. Detect sticky/fixed positioning
4. Identify scroll-snap containers
5. Check for smooth scroll libraries (Lenis class, Locomotive Scroll)

### Image/Asset Handling

1. Discover all `<img>` elements and their `src` attributes
2. Detect background-image CSS properties
3. Identify inline SVGs and extract their markup
4. Detect layered compositions (multiple positioned images with z-index)
5. Download assets to `public/` directory

### Output Format

- **NOT** raw HTML/CSS
- Generates a full **Next.js 16 + Tailwind CSS v4** project
- Component spec files at `docs/research/components/<Name>.spec.md`
- Each component gets its own React component file
- Uses `next/font` for font loading
- Uses Tailwind utilities mapped from computed CSS values

### Limitations Documented

- **SPAs with client-side routing** — may not capture all routes
- **Auth-walled content** — cannot access pages behind login
- **Heavy JS-rendered content** — needs page to fully render before extraction
- **CSS-in-JS** — computed styles work, but variable names and theme tokens are lost
- **Animations** — captures keyframes but timing/easing may need manual tuning
- **Third-party embeds** — iframes, embedded videos may not clone correctly

### Key Architectural Insight

The JCodesMore skill is **entirely a prompt** — zero executable code. It instructs Claude Code to:
1. Use browser MCP to navigate and extract
2. Use its own code generation abilities to produce React/Next.js
3. Use sub-agents (parallel builders in git worktrees) for parallelism
4. Use visual comparison for QA

There is no Python, no Node.js script, no utility library. The skill's value is in the QUALITY OF THE PROMPT — the specific extraction steps, the ordering, the completeness checks, and the lessons encoded from failed clones.
