# Gap Analysis: Our Playwright MCP vs Open Source Cloner

## Our Playwright MCP Tools Available

From `.mcp.json` — we use `@playwright/mcp` (Microsoft's official Playwright MCP server).

Available tools (confirmed from MCP tool list):
| Tool | Purpose |
|------|---------|
| `browser_navigate` | Navigate to URL |
| `browser_snapshot` | Get accessibility tree / DOM snapshot |
| `browser_take_screenshot` | Capture page screenshot |
| `browser_click` | Click elements |
| `browser_hover` | Hover over elements |
| `browser_fill_form` | Fill form fields |
| `browser_select_option` | Select dropdown options |
| `browser_press_key` | Press keyboard keys |
| `browser_type` | Type text |
| `browser_evaluate` | Execute JavaScript in page context |
| `browser_run_code` | Run Playwright code snippets |
| `browser_wait_for` | Wait for conditions |
| `browser_resize` | Resize viewport |
| `browser_navigate_back` | Go back |
| `browser_tabs` | Manage browser tabs |
| `browser_close` | Close browser |
| `browser_console_messages` | Read console output |
| `browser_network_requests` | Monitor network traffic |
| `browser_drag` | Drag elements |
| `browser_file_upload` | Upload files |
| `browser_handle_dialog` | Handle alerts/confirms |
| `browser_install` | Install browsers |

## Capability Comparison

| Capability | Open Source Repo (JCodesMore) | Our Playwright MCP | Gap? |
|-----------|-------------------------------|-------------------|------|
| Navigate to URL | browser_navigate | `browser_navigate` | **No gap** |
| Full-page screenshots | browser_screenshot | `browser_take_screenshot` | **No gap** |
| DOM snapshot | browser_snapshot | `browser_snapshot` | **No gap** |
| Extract computed styles via JS | browser_evaluate + getComputedStyle() | `browser_evaluate` + same JS | **No gap** |
| Extract fonts | browser_evaluate + document.fonts | `browser_evaluate` + same JS | **No gap** |
| Extract CSS variables | browser_evaluate + getComputedStyle() | `browser_evaluate` + same JS | **No gap** |
| Extract media queries | browser_evaluate + document.styleSheets | `browser_evaluate` + same JS | **No gap** |
| Click interactive elements | browser_click | `browser_click` | **No gap** |
| Hover for states | Not explicitly documented | `browser_hover` | **No gap** (we have MORE) |
| Resize viewport | browser_resize | `browser_resize` | **No gap** |
| Network monitoring | Not documented | `browser_network_requests` | **We have MORE** |
| Download images | Via asset script | `browser_evaluate` + fetch | **No gap** — different method, same result |
| Handle responsive | Resize + re-extract | `browser_resize` + re-extract | **No gap** |
| Generate clean HTML/CSS | Claude Code generation | Claude Code generation | **No gap** |
| Parallel builder agents | git worktrees + sub-agents | Sub-agents available | **No gap** |
| Visual QA comparison | Screenshots + Claude vision | Screenshots + Claude vision | **No gap** |

## Assessment: What Does the Open Source Repo Actually Add?

**The open source skill is a well-crafted prompt, NOT new functionality.**

It adds ZERO actual capabilities beyond what our Playwright MCP already provides. Every extraction technique it uses maps directly to `browser_evaluate` + JavaScript. The value is entirely in:

1. **Structured extraction prompts** — The exact JavaScript snippets to run via `browser_evaluate` for comprehensive extraction
2. **Sequencing knowledge** — The order of operations (screenshot first, then extract globals, then per-component)
3. **Completeness checks** — Reminders to check multi-state, scroll behaviors, layered images, smooth scroll libraries
4. **Anti-pattern documentation** — What NOT to do (don't guess CSS, don't skip hover states, don't miss overlays)
5. **Output organization** — How to structure the generated code (spec files, component files, assembly)

## Key Difference: Output Target

The JCodesMore repo targets **Next.js + Tailwind CSS** output. Our skill can target **plain HTML/CSS** — which is simpler, more portable, and doesn't require a React build toolchain.

This is actually an advantage for our use case: the user wants to clone a site for reference/prototyping, not build a production React app from it.

## Conclusion

**Option B (thin wrapper)** is the correct approach. We need:
1. A SKILL.md that teaches Claude the extraction steps (the "what to extract" knowledge)
2. Reference files with the specific `browser_evaluate` JavaScript snippets
3. A `/clone` command as the entry point
4. Output format: clean HTML + CSS + assets folder (simpler than Next.js)

We do NOT need to fork, install, or depend on any external repo. Our Playwright MCP already has every tool needed.
