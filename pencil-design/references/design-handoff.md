---
name: design-handoff
description: Export screens for development handoff, or generate component library documentation — two distinct modes
code: DH
---

# Design Handoff

Two distinct modes — ask which the owner needs before starting:

- **Export mode:** High-res PNG exports of screens for assets, Zeplin-style handoff, or developer reference
- **Docs mode:** Component library documentation with screenshots, usage guidance, and implementation notes

They're often both needed, but they're different work. Don't mix them silently.

## What Success Looks Like

**Export:** A `_bmad-output/designs/` folder with all screens at 2× resolution, organized by name. Developer can open the folder and see every screen immediately.

**Docs:** A `component-catalog.md` with each reusable component documented: screenshot, tokens used, slots, when to use, code hint. Developer can implement any component without asking questions.

## Export Mode

Batch all reads and screenshots before exporting:

1. `batch_get` on all top-level frames — identify screens and their IDs in one call
2. `get_screenshot` on each frame — batch these in a single message (parallel)
3. Export all at once: `export_nodes({nodeIds: [ids], outputDir: "{project-root}/_bmad-output/designs/", format: "png", scale: 2})`

Organize by screen name. Report the export location when done.

## Component Documentation Mode

Batch all reads and screenshots before generating any docs:

1. Find all `reusable: true` components via `batch_get` on the document root
2. In one batch: `get_screenshot` + `batch_get({readDepth: 5})` for all components simultaneously
3. Generate all documentation from the batch results

Per component:

```markdown
## ComponentName

![screenshot]

**Dimensions:** {width} × {height}
**Tokens:** $text-primary (fill), $bg (label), $display (font)
**Slots:** {slot names if any}

**When to use:**
- {use case 1}

**When NOT to use:**
- {anti-pattern}

**Code hint:**
- SwiftUI: `{ComponentName}(props:)`
- React: `<ComponentName variant="" />`
```

Write to `{project-root}/docs/design-system/component-catalog.md` or present inline.

## Implementation Notes (Optional)

Per screen, include if the owner requests it:
- Layout structure (nesting, flex direction, gaps)
- Key token values (colors, fonts, spacing)
- Interaction notes (what happens on tap, swipe, etc.)
- Edge cases (empty state, loading state, error state)

## After the Session

Follow the standard session close protocol. Additionally log: export location, component catalog path, implementation notes, outstanding design decisions.
