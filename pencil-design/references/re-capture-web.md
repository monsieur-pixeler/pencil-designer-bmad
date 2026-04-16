---
name: re-capture-web
description: "Sub-reference for [RE] — Web app capture via Chrome DevTools MCP"
parent: reverse-engineer
---

# Web App Capture (Chrome DevTools MCP) — Fully Automated

This is the most powerful path. We can extract actual CSS values, not just pixel-guess.

**Step 1 — Initial scan:**

```
1. navigate_page({url: "..."})
2. take_screenshot() — capture the landing/home state
3. evaluate_script({expression: `JSON.stringify({
     colors: [...new Set([...document.querySelectorAll('*')].flatMap(el => {
       const s = getComputedStyle(el);
       return [s.color, s.backgroundColor, s.borderColor].filter(c => c !== 'rgba(0, 0, 0, 0)');
     })))],
     fonts: [...new Set([...document.querySelectorAll('*')].map(el => {
       const s = getComputedStyle(el);
       return s.fontFamily.split(',')[0].trim().replace(/['"]/g, '');
     })))],
     spacing: [...new Set([...document.querySelectorAll('*')].flatMap(el => {
       const s = getComputedStyle(el);
       return [s.gap, s.padding, s.margin].filter(v => v && v !== '0px');
     })))]
   })`})
```

This gives us the real CSS token palette in one call.

**Step 2 — Screen inventory:**

Navigate each major route. For SPAs:

```
evaluate_script({expression: `
  // Extract all internal links
  JSON.stringify([...document.querySelectorAll('a[href]')]
    .map(a => a.href)
    .filter(h => h.startsWith(location.origin))
    .filter((v,i,a) => a.indexOf(v) === i)
  )
`})
```

For each unique route: `navigate_page` → `take_screenshot` → save.

**Step 3 — Component extraction (DOM-level):**

```
evaluate_script({expression: `
  // Find repeated structural patterns
  const patterns = {};
  document.querySelectorAll('[class]').forEach(el => {
    const cls = [...el.classList].sort().join(' ');
    if (!patterns[cls]) patterns[cls] = { count: 0, tag: el.tagName, sample: el.outerHTML.substring(0, 200) };
    patterns[cls].count++;
  });
  JSON.stringify(Object.entries(patterns)
    .filter(([_, v]) => v.count >= 3)
    .sort((a, b) => b[1].count - a[1].count)
    .slice(0, 20)
    .map(([cls, v]) => ({ class: cls, count: v.count, tag: v.tag }))
  )
`})
```

**Step 4 — Responsive capture (optional):**

```
// Capture at multiple viewport sizes
emulate({device: "iPhone 12"})  → take_screenshot()
emulate({device: "iPad"})       → take_screenshot()
resize_page({width: 1440, height: 900}) → take_screenshot()
```

## Platform Tips — Getting the Most Data

- Use `evaluate_script` to extract CSS custom properties (`:root` variables) — these ARE the design tokens
- Check for Tailwind: `evaluate_script` to read `tailwind.config` if it's exposed
- Extract SVG icons and their names for icon mapping
- Check responsive breakpoints: resize viewport and capture at each breakpoint
