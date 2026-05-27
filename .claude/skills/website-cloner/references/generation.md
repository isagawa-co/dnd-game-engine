# Generation Reference — HTML/CSS from Extracted Data

How to convert extracted page data into clean, self-contained HTML and CSS.

---

## Section: Generate

### HTML Generation Rules

1. **Use semantic tags.** Map extracted sections to appropriate HTML5 elements:
   - Site header with nav -> `<header>` + `<nav>`
   - Hero/banner area -> `<section class="hero">`
   - Main content -> `<main>`
   - Content sections -> `<section>`
   - Cards/items -> `<article>`
   - Footer -> `<footer>`

2. **Use real text content.** Copy the actual text from the extraction (from `textContent` in the DOM snapshot). Never use placeholder text.

3. **Class naming.** Use descriptive BEM-style classes derived from the page structure:
   - `.header`, `.header__nav`, `.header__logo`
   - `.hero`, `.hero__title`, `.hero__subtitle`
   - `.features`, `.features__card`, `.features__icon`

4. **Image references.** Point `src` attributes to local paths: `assets/images/filename.ext`

5. **Font loading.** Add Google Fonts `<link>` tags in `<head>` if the site uses Google Fonts. For self-hosted fonts, reference local copies via `@font-face` in CSS.

6. **Meta tags.** Include viewport meta, charset, and title extracted from the original page:
   ```html
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>[extracted title]</title>
   <link rel="stylesheet" href="styles.css">
   ```

### CSS Generation Rules

1. **CSS custom properties first.** Define all colors, fonts, and spacing as variables at the top of `styles.css`:
   ```css
   :root {
     /* Colors — from extracted customProperties + computed values */
     --color-primary: #...;
     --color-text: #...;
     --color-bg: #...;

     /* Fonts — from font extraction */
     --font-heading: 'Inter', sans-serif;
     --font-body: 'Inter', sans-serif;

     /* Spacing — from computed padding/margin patterns */
     --spacing-sm: 8px;
     --spacing-md: 16px;
     --spacing-lg: 32px;
     --spacing-xl: 64px;
   }
   ```

2. **Organize by component.** Group CSS rules by the section they belong to:
   ```css
   /* === Header === */
   .header { ... }
   .header__nav { ... }

   /* === Hero === */
   .hero { ... }

   /* === Features === */
   .features { ... }
   ```

3. **Use extracted values exactly.** Every `color`, `font-size`, `padding`, `margin`, `gap`, `border-radius` comes from `getComputedStyle()` output. Convert RGB to hex where cleaner. Use the exact pixel values.

4. **Layout with flexbox/grid.** Replicate the extracted `display`, `flex-direction`, `justify-content`, `align-items`, `gap`, `grid-template-columns` properties.

5. **No inline styles.** Every style goes in `styles.css`. HTML elements only have `class` attributes.

6. **Hover/focus states.** If extracted, include them:
   ```css
   .button:hover {
     background-color: var(--color-primary-hover);
     transform: translateY(-1px);
   }
   ```

---

## Section: Assets

### Image Download

For each image found during extraction:

1. Create the directory: `[output-dir]/assets/images/`
2. Use `browser_evaluate` to fetch images as base64 and write them:
   ```javascript
   // Run via browser_evaluate for each image URL
   (async (url) => {
     const response = await fetch(url);
     const blob = await response.blob();
     return new Promise((resolve) => {
       const reader = new FileReader();
       reader.onloadend = () => resolve(reader.result);
       reader.readAsDataURL(blob);
     });
   })('https://target-site.com/image.jpg')
   ```
3. Alternatively, use the image URL directly if it's publicly accessible and download via Bash:
   ```bash
   curl -o "[output-dir]/assets/images/filename.jpg" "https://target-site.com/image.jpg"
   ```

### SVG Handling

For inline SVGs extracted during the extraction phase:
- Save each SVG to `assets/images/icon-[name].svg`
- Reference in HTML as `<img src="assets/images/icon-[name].svg">`
- For decorative SVGs, inline them directly in the HTML

### Font Handling

| Font Source | Action |
|------------|--------|
| Google Fonts | Add `<link>` tag in HTML `<head>` with the extracted URL |
| Adobe Fonts (Typekit) | Add the `<link>` tag from the extracted URL |
| Self-hosted (@font-face) | Download font files to `assets/fonts/`, write `@font-face` rules in CSS |
| System fonts | No action needed — just reference in `font-family` |

---

## Section: Output

### File Structure

```
[output-dir]/
  index.html          ← Complete HTML page
  styles.css          ← All CSS (variables, components, responsive)
  assets/
    images/           ← Downloaded images and SVGs
    fonts/            ← Self-hosted font files (if any)
```

### index.html Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Page Title]</title>
  <!-- Google Fonts (if used) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=[Font]+[Params]" rel="stylesheet">
  <!-- Stylesheet -->
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="header">
    <!-- Extracted header content -->
  </header>

  <main>
    <section class="hero">
      <!-- Extracted hero content -->
    </section>

    <section class="[section-name]">
      <!-- Extracted section content -->
    </section>
  </main>

  <footer class="footer">
    <!-- Extracted footer content -->
  </footer>
</body>
</html>
```

### styles.css Template

```css
/* === Reset === */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* === Custom Properties === */
:root {
  /* Populated from extraction */
}

/* === Base === */
body {
  font-family: var(--font-body);
  color: var(--color-text);
  background-color: var(--color-bg);
  line-height: [extracted];
}

/* === Components (one section per component) === */

/* === Responsive === */
@media (max-width: [breakpoint]px) {
  /* Layout changes extracted from responsive comparison */
}
```

---

## Section: QA

After generating the output:

1. **Open the cloned page in the browser:**
   ```
   Tool: browser_navigate
   Args: { "url": "file:///[absolute-path]/index.html" }
   ```

2. **Take a screenshot of the clone** at 1440px and 390px

3. **Compare visually** with the reference screenshots taken during extraction

4. **Fix discrepancies:**
   - Color mismatches -> check CSS variable values
   - Layout shifts -> check flex/grid properties
   - Missing images -> verify download paths
   - Wrong fonts -> check Google Fonts link or @font-face
   - Spacing issues -> check padding/margin values

5. **Iterate** until the clone matches the original at both desktop and mobile widths

---

## Quality Checklist

Before declaring the clone complete:

- [ ] `index.html` opens in browser without errors
- [ ] No inline styles — all CSS in `styles.css`
- [ ] Semantic HTML tags used (not div soup)
- [ ] All images downloaded and loading from local `assets/`
- [ ] Fonts loading correctly (check browser dev tools)
- [ ] Responsive layout works at desktop and mobile widths
- [ ] Colors match the original (spot-check 3-5 elements)
- [ ] Text content matches the original (not placeholder)
