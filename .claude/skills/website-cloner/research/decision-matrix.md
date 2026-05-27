# Decision Matrix: Website Cloner Approaches

## Capability Comparison

| Capability | Open Source (JCodesMore) | Our Playwright MCP | Gap? |
|-----------|--------------------------|-------------------|------|
| Navigate to URL | `browser_navigate` | `browser_navigate` | No |
| Extract computed styles | `browser_evaluate` + `getComputedStyle()` | `browser_evaluate` + `getComputedStyle()` | No |
| Extract fonts | `browser_evaluate` + `document.fonts` + stylesheet scan | `browser_evaluate` + same JS | No |
| Extract layout | `browser_evaluate` + flex/grid property extraction | `browser_evaluate` + same JS | No |
| Download images | Asset discovery script (via browser) | `browser_evaluate` + fetch / `browser_network_requests` | No |
| Handle responsive | `browser_resize` at 1440/768/390 | `browser_resize` at any width | No |
| Generate clean HTML/CSS | Claude Code generates Next.js + Tailwind | Claude Code generates HTML + CSS | No (different target) |
| Multi-state extraction | Click tabs, scroll, hover — multi-pass | `browser_click` + `browser_hover` + `browser_evaluate` | No |
| Scroll behavior detection | Lenis/Locomotive class detection | `browser_evaluate` + same JS | No |
| Screenshot comparison | `browser_take_screenshot` + Claude vision | `browser_take_screenshot` + Claude vision | No |
| Parallel builder agents | Git worktrees + sub-agents | Sub-agents available | No |
| Network monitoring | Not documented | `browser_network_requests` | We have more |
| Console inspection | Not documented | `browser_console_messages` | We have more |

## Scoring

| Criterion | Option A: Fork/Adapt | Option B: Thin Wrapper | Option C: Build from Scratch |
|-----------|---------------------|----------------------|----------------------------|
| Implementation effort | Medium (strip Next.js, rewrite for HTML) | Low (write skill + references) | High (reinvent extraction logic) |
| Maintenance burden | High (track upstream changes) | Low (self-contained) | Medium (all on us) |
| Output flexibility | Low (locked to Next.js) | High (HTML/CSS, portable) | High (any format) |
| Extraction quality | High (battle-tested prompts) | High (borrow extraction knowledge) | Medium (learning from scratch) |
| Dependency risk | Medium (external repo) | None | None |
| Time to first clone | 1-2 hours (adapt) | 30 min (write skill) | 3-4 hours (research + build) |

## Winner: Option B (Thin Wrapper)

**Score: 5/6 best ratings across criteria.**

We borrow the extraction knowledge (what JS to run, what to look for, what pitfalls to avoid) and encode it in our own skill files. We target clean HTML/CSS instead of Next.js. Zero external dependencies.
