# Extraction Reference — Playwright MCP Calls

How to extract page data from a live website using Playwright MCP tools.

---

## Step 1: Navigate

Use `browser_navigate` to load the target URL.

```
Tool: browser_navigate
Args: { "url": "https://target-site.com" }
```

Wait for the page to fully load. If the site uses client-side rendering, use `browser_wait_for` to wait for key elements:

```
Tool: browser_wait_for
Args: { "selector": "main", "state": "visible", "timeout": 10000 }
```

---

## Step 2: Screenshot (Desktop + Mobile)

Take reference screenshots at two viewport widths for later QA comparison.

**Desktop (1440px):**
```
Tool: browser_resize
Args: { "width": 1440, "height": 900 }

Tool: browser_take_screenshot
```

**Mobile (390px):**
```
Tool: browser_resize
Args: { "width": 390, "height": 844 }

Tool: browser_take_screenshot
```

Reset to desktop width for extraction:
```
Tool: browser_resize
Args: { "width": 1440, "height": 900 }
```

---

## Step 3: Extract Page Structure

Use `browser_snapshot` to get the accessibility tree / DOM structure:

```
Tool: browser_snapshot
```

This returns the semantic structure of the page — headings, navigation, main content areas, footer. Use this to plan the HTML structure.

---

## Step 4: Extract Styles via JavaScript

Use `browser_evaluate` to run JavaScript in the page context. Run each extraction script separately.

### 4a: Global Styles (Colors, Fonts, Spacing)

```javascript
// Run via browser_evaluate
(() => {
  const body = document.body;
  const bodyStyles = window.getComputedStyle(body);

  // Extract CSS custom properties from :root
  const rootStyles = window.getComputedStyle(document.documentElement);
  const customProps = {};
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule.selectorText === ':root') {
          for (const prop of rule.style) {
            if (prop.startsWith('--')) {
              customProps[prop] = rule.style.getPropertyValue(prop).trim();
            }
          }
        }
      }
    } catch(e) { /* cross-origin stylesheet, skip */ }
  }

  return {
    backgroundColor: bodyStyles.backgroundColor,
    color: bodyStyles.color,
    fontFamily: bodyStyles.fontFamily,
    fontSize: bodyStyles.fontSize,
    lineHeight: bodyStyles.lineHeight,
    customProperties: customProps
  };
})()
```

### 4b: Font Discovery

```javascript
// Run via browser_evaluate
(() => {
  const fonts = [];

  // 1. Check loaded fonts via document.fonts API
  for (const font of document.fonts) {
    fonts.push({
      family: font.family,
      weight: font.weight,
      style: font.style,
      status: font.status
    });
  }

  // 2. Find Google Fonts / Adobe Fonts links
  const fontLinks = [];
  document.querySelectorAll('link[href*="fonts.googleapis.com"], link[href*="fonts.gstatic.com"], link[href*="use.typekit.net"]').forEach(link => {
    fontLinks.push(link.href);
  });

  // 3. Extract @font-face declarations
  const fontFaces = [];
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule instanceof CSSFontFaceRule) {
          fontFaces.push({
            family: rule.style.getPropertyValue('font-family'),
            src: rule.style.getPropertyValue('src'),
            weight: rule.style.getPropertyValue('font-weight'),
            style: rule.style.getPropertyValue('font-style')
          });
        }
      }
    } catch(e) { /* cross-origin */ }
  }

  return { loadedFonts: fonts, fontLinks, fontFaces };
})()
```

### 4c: Section-by-Section Computed Styles

For each major section (header, hero, features, footer, etc.), extract computed styles:

```javascript
// Run via browser_evaluate — adapt selector for each section
((selector) => {
  const el = document.querySelector(selector);
  if (!el) return null;

  const styles = window.getComputedStyle(el);
  const children = [];

  // Extract styles for direct children too
  el.querySelectorAll(':scope > *').forEach((child, i) => {
    const cs = window.getComputedStyle(child);
    children.push({
      tag: child.tagName.toLowerCase(),
      classes: child.className,
      text: child.textContent?.substring(0, 100),
      styles: {
        display: cs.display,
        position: cs.position,
        width: cs.width,
        height: cs.height,
        padding: cs.padding,
        margin: cs.margin,
        color: cs.color,
        backgroundColor: cs.backgroundColor,
        fontSize: cs.fontSize,
        fontWeight: cs.fontWeight,
        fontFamily: cs.fontFamily,
        lineHeight: cs.lineHeight,
        textAlign: cs.textAlign,
        flexDirection: cs.flexDirection,
        justifyContent: cs.justifyContent,
        alignItems: cs.alignItems,
        gap: cs.gap,
        gridTemplateColumns: cs.gridTemplateColumns,
        borderRadius: cs.borderRadius,
        boxShadow: cs.boxShadow,
        opacity: cs.opacity,
        transform: cs.transform,
        transition: cs.transition
      }
    });
  });

  return {
    tag: el.tagName.toLowerCase(),
    styles: {
      display: styles.display,
      position: styles.position,
      width: styles.width,
      maxWidth: styles.maxWidth,
      padding: styles.padding,
      margin: styles.margin,
      backgroundColor: styles.backgroundColor,
      flexDirection: styles.flexDirection,
      justifyContent: styles.justifyContent,
      alignItems: styles.alignItems,
      gap: styles.gap,
      gridTemplateColumns: styles.gridTemplateColumns
    },
    childCount: children.length,
    children: children
  };
})('header')  // Change selector for each section
```

### 4d: Media Query Breakpoints

```javascript
// Run via browser_evaluate
(() => {
  const breakpoints = new Set();
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule instanceof CSSMediaRule) {
          const match = rule.conditionText.match(/(\d+)px/g);
          if (match) match.forEach(bp => breakpoints.add(bp));
        }
      }
    } catch(e) { /* cross-origin */ }
  }
  return { breakpoints: [...breakpoints].sort((a,b) => parseInt(a) - parseInt(b)) };
})()
```

### 4e: Image & SVG Extraction

```javascript
// Run via browser_evaluate
(() => {
  const images = [];

  // <img> elements
  document.querySelectorAll('img').forEach(img => {
    images.push({
      type: 'img',
      src: img.src,
      alt: img.alt,
      width: img.naturalWidth,
      height: img.naturalHeight
    });
  });

  // Background images
  document.querySelectorAll('*').forEach(el => {
    const bg = window.getComputedStyle(el).backgroundImage;
    if (bg && bg !== 'none') {
      const urlMatch = bg.match(/url\("?(.+?)"?\)/);
      if (urlMatch) {
        images.push({
          type: 'background-image',
          src: urlMatch[1],
          element: el.tagName.toLowerCase() + (el.className ? '.' + el.className.split(' ')[0] : '')
        });
      }
    }
  });

  // Inline SVGs
  const svgs = [];
  document.querySelectorAll('svg').forEach((svg, i) => {
    svgs.push({
      index: i,
      viewBox: svg.getAttribute('viewBox'),
      width: svg.getAttribute('width'),
      height: svg.getAttribute('height'),
      markup: svg.outerHTML.substring(0, 2000) // Truncate large SVGs
    });
  });

  return { images, svgs };
})()
```

---

## Step 4f: Sanity Check — Detect Non-DOM Rendering

After extracting typography via `getComputedStyle()`, run a sanity check. If all elements return identical defaults, the site likely renders via canvas, SVG text, or deferred-hydration components.

```javascript
// Run via browser_evaluate
(() => {
  const selectors = ['h1', 'h2', 'h3', 'p', 'a', 'button', 'span'];
  const results = [];

  for (const sel of selectors) {
    const el = document.querySelector(sel);
    if (el) {
      const cs = window.getComputedStyle(el);
      results.push({
        selector: sel,
        fontSize: cs.fontSize,
        lineHeight: cs.lineHeight,
        fontWeight: cs.fontWeight
      });
    }
  }

  if (results.length < 3) {
    return { flagged: false, reason: 'Too few elements found to check', values: results };
  }

  const first = results[0];
  const allIdentical = results.every(r =>
    r.fontSize === first.fontSize &&
    r.lineHeight === first.lineHeight &&
    r.fontWeight === first.fontWeight
  );

  return {
    flagged: allIdentical,
    reason: allIdentical
      ? 'All elements returned identical typography defaults — likely non-DOM rendering (canvas, SVG text, or deferred hydration)'
      : 'Typography values vary across elements — DOM extraction is reliable',
    values: results
  };
})()
```

**If `flagged: true`:** Proceed to the fallback strategies below (Hydration Wait → SVG Text Extraction → Canvas Detection) before accepting the extracted values. The DOM values are defaults, not the actual visual rendering.

**If `flagged: false`:** The extracted values are reliable. Skip fallback strategies and continue to Step 5.

---

## Fallback Strategy 1: Hydration Wait

When the sanity check flags identical defaults, the site may use deferred-hydration React/Next.js components. Wait for hydration to complete, then re-extract.

```javascript
// Run via browser_evaluate
(() => {
  return new Promise((resolve) => {
    let mutationCount = 0;
    let settleTimer = null;

    const observer = new MutationObserver((mutations) => {
      mutationCount += mutations.length;
      clearTimeout(settleTimer);
      settleTimer = setTimeout(() => {
        observer.disconnect();
        resolve({
          waited: true,
          mutations_detected: mutationCount,
          settled: true
        });
      }, 2000); // Consider settled after 2s of no mutations
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
      attributes: true,
      characterData: true
    });

    // Fallback timeout — don't wait forever
    setTimeout(() => {
      observer.disconnect();
      resolve({
        waited: true,
        mutations_detected: mutationCount,
        settled: mutationCount === 0
      });
    }, 5000);
  });
})()
```

**After waiting:** Re-run the Step 4c section extraction and re-check with the sanity check (Step 4f). If values now vary, hydration was the issue — use the new values. If still identical, proceed to SVG Text Extraction.

**Note:** This is best-effort. Some sites require user interaction (scroll, click) to trigger hydration.

---

## Fallback Strategy 2: SVG Text Extraction

Some sites render headlines inside `<svg>` elements using `<text>` tags. `getComputedStyle()` on CSS selectors won't capture these.

```javascript
// Run via browser_evaluate
(() => {
  const svgTexts = [];

  document.querySelectorAll('svg text, svg tspan').forEach((el) => {
    const bbox = el.getBBox ? el.getBBox() : null;
    svgTexts.push({
      text: el.textContent?.substring(0, 200),
      fontSize: el.getAttribute('font-size') || el.style.fontSize || (bbox ? Math.round(bbox.height) + 'px' : null),
      fontFamily: el.getAttribute('font-family') || el.style.fontFamily || null,
      fontWeight: el.getAttribute('font-weight') || el.style.fontWeight || null,
      fill: el.getAttribute('fill') || el.style.fill || null,
      x: el.getAttribute('x'),
      y: el.getAttribute('y')
    });
  });

  // Sort by font size descending to infer role (largest = h1, etc.)
  svgTexts.sort((a, b) => {
    const sizeA = parseInt(a.fontSize) || 0;
    const sizeB = parseInt(b.fontSize) || 0;
    return sizeB - sizeA;
  });

  return {
    svg_text_found: svgTexts.length > 0,
    elements: svgTexts
  };
})()
```

**Mapping SVG text to typography roles:** Use the sorted list — the largest font size maps to `h1`, second largest to `h2`, and so on. Use SVG text attributes as the typography values when DOM extraction returned defaults.

**If `svg_text_found: false`:** Proceed to Canvas Detection.

---

## Fallback Strategy 3: Canvas Detection

Some sites render content via `<canvas>` elements (WebGL, Three.js). Canvas pixels cannot be extracted via DOM APIs.

```javascript
// Run via browser_evaluate
(() => {
  const canvases = [];
  const viewportArea = window.innerWidth * window.innerHeight;

  document.querySelectorAll('canvas').forEach((canvas, i) => {
    const rect = canvas.getBoundingClientRect();
    const area = rect.width * rect.height;
    let hasWebGL = false;

    try {
      hasWebGL = !!(canvas.getContext('webgl') || canvas.getContext('webgl2'));
    } catch(e) { /* context already acquired */ }

    canvases.push({
      index: i,
      width: rect.width,
      height: rect.height,
      area: area,
      viewportRatio: (area / viewportArea).toFixed(2),
      hasWebGL: hasWebGL
    });
  });

  const totalCanvasArea = canvases.reduce((sum, c) => sum + c.area, 0);
  const dominant = totalCanvasArea / viewportArea > 0.5;

  return {
    canvas_found: canvases.length > 0,
    elements: canvases,
    dominant: dominant
  };
})()
```

**If `dominant: true` (canvas covers >50% viewport):** Typography extraction is unreliable for canvas-rendered sections. Mark canvas content as "unextractable" — do not attempt to clone the canvas rendering. Use screenshot-based estimation or skip typography for those sections.

**If `canvas_found: true` but `dominant: false`:** Canvas is decorative (background animation, particle effects). DOM extraction is still valid for text content.

---

## Step 4g: Custom Property vs Computed Style Divergence

CSS custom properties (`:root` variables) and computed styles can diverge — for example, `--background: #fff` vs computed `rgb(0, 0, 0)` due to dark mode toggles or media queries.

```javascript
// Run via browser_evaluate
(() => {
  const rootStyles = window.getComputedStyle(document.documentElement);
  const bodyStyles = window.getComputedStyle(document.body);
  const divergences = [];

  // Get custom properties from :root
  const customProps = {};
  for (const sheet of document.styleSheets) {
    try {
      for (const rule of sheet.cssRules) {
        if (rule.selectorText === ':root') {
          for (const prop of rule.style) {
            if (prop.startsWith('--')) {
              customProps[prop] = rule.style.getPropertyValue(prop).trim();
            }
          }
        }
      }
    } catch(e) { /* cross-origin */ }
  }

  // Compare color-related custom properties against computed values
  const colorProps = Object.entries(customProps).filter(([k, v]) =>
    k.includes('color') || k.includes('bg') || k.includes('background') ||
    v.startsWith('#') || v.startsWith('rgb') || v.startsWith('hsl')
  );

  for (const [prop, declared] of colorProps) {
    const resolved = rootStyles.getPropertyValue(prop).trim();
    if (resolved && resolved !== declared) {
      divergences.push({ property: prop, declared, resolved, source: ':root' });
    }
  }

  // Check for prefers-color-scheme media queries
  const darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;

  // Compare body background
  const bgCustom = customProps['--background'] || customProps['--bg'] || customProps['--background-color'];
  const bgComputed = bodyStyles.backgroundColor;
  if (bgCustom && bgComputed && bgCustom !== bgComputed) {
    divergences.push({ property: '--background', declared: bgCustom, resolved: bgComputed, source: 'body' });
  }

  return {
    divergences: divergences,
    likely_dark_mode: darkMode,
    custom_property_count: Object.keys(customProps).length
  };
})()
```

**Resolving divergences:** When a custom property value differs from the computed value, prefer the **computed value** (what the user actually sees). Note the custom property as the "light mode" or "alternate" value in the extracted data. If `likely_dark_mode: true`, the divergence is expected — document both values.

---

## Step 5: Extract Interactive States (Optional)

If the page has interactive elements (nav dropdowns, tabs, accordions):

1. Use `browser_hover` on interactive elements and re-extract styles
2. Use `browser_click` on tabs/buttons and capture the changed state
3. Compare before/after styles to determine hover effects and transitions

```
Tool: browser_hover
Args: { "selector": ".nav-link" }

Tool: browser_evaluate
Args: { "expression": "/* re-extract computed styles for hovered element */" }
```

---

## Step 6: Extract Responsive Layout

Resize to mobile and re-extract layout properties:

```
Tool: browser_resize
Args: { "width": 768, "height": 1024 }

Tool: browser_evaluate
Args: { "expression": "/* re-run section extraction at tablet width */" }

Tool: browser_resize
Args: { "width": 390, "height": 844 }

Tool: browser_evaluate
Args: { "expression": "/* re-run section extraction at mobile width */" }
```

Compare desktop vs mobile layouts to determine which properties change at each breakpoint.

---

## Edge Cases

| Case | How to Handle |
|------|---------------|
| Lazy-loaded images | Scroll to bottom first via `browser_evaluate` with `window.scrollTo(0, document.body.scrollHeight)`, wait, then extract |
| CSS-in-JS (styled-components, emotion) | `getComputedStyle()` still works — it reads final computed values regardless of how CSS was authored |
| Web fonts from CDN | Extract the Google Fonts URL and include as `<link>` in output HTML |
| Self-hosted fonts | Download the font files to `assets/fonts/` and create `@font-face` declarations |
| iframes / embeds | Note their presence but don't attempt to clone iframe content |
| JavaScript-rendered content | Use `browser_wait_for` to ensure content is rendered before extracting |
| Very long pages | Extract in sections — scroll to each section, extract, move to next |
| Canvas-rendered content | Run canvas detection (Step 4f fallback 3). Mark as unextractable — do not attempt to clone canvas pixels |
| SVG text rendering | Run SVG text extraction (Step 4f fallback 2). Map SVG `<text>` attributes to typography roles |
| Deferred hydration (React/Next.js) | Run hydration wait (Step 4f fallback 1). Wait for DOM mutations to settle, then re-extract |
| All typography values identical | Sanity check flagged (Step 4f). Use fallback strategies before accepting defaults |
| CSS custom property divergence | Compare `getPropertyValue()` vs `getComputedStyle()` (Step 4g). Prefer computed value, note alternate |
