---
name: responsive-preview
description: Preview a screen at multiple device sizes to verify responsive behavior
code: RP
---

# Responsive Preview

Generate previews of a screen at multiple standard device sizes to verify it works across breakpoints before code is written.

## What Success Looks Like

Screenshots of the same screen at each requested device size, laid out in a comparison row. The owner can see how content reflows across sizes and catch issues before implementation.

## Standard Device Sizes

| Device | Width | Height |
|---|---|---|
| iPhone SE | 375px | 667px |
| iPhone 15 | 393px | 852px |
| iPhone 15 Plus | 430px | 932px |
| iPad Air | 820px | 1180px |
| iPad Pro 13" | 1024px | 1366px |
| MacBook 13" | 1280px | 800px |
| MacBook Pro 16" | 1440px | 900px |

## Process

1. Read source frame and batch all canvas position queries before creating any frames:
   - `batch_get({nodeIds: [id], readDepth: 5})` — read source frame structure
   - In one batch: call `find_empty_space_on_canvas` for each target size position (all positions resolved before any frame is created)
2. Create all target frames from the pre-fetched positions
3. Copy and adapt the content for each:
   - **Quick preview (same layout):** Different frame dimensions only — shows overflow/clipping behavior
   - **Full recomposition (different breakpoint):** Content restructured for platform interaction model — load `[MP]` for this
4. Screenshot all frames in a single batch
5. Present as a comparison row with device labels

## Output

```
Responsive Preview: Dashboard

[iPhone 15 — 393px] [iPad Air — 820px] [MacBook 13" — 1280px]
   ↑ approves           ↑ needs sidebar      ↑ needs sidebar + detail panel
```

## Quick vs. Full — Choosing Between [RP] and [MP]

| Use [RP] when... | Use [MP] when... |
|---|---|
| Checking if content clips or overflows at larger sizes | Creating a genuinely different layout for iPad/macOS/web |
| Verifying breakpoint thresholds | Restructuring navigation (tab bar → sidebar) |
| Quick sanity check across device widths | Recomposing content blocks into multi-column layouts |
| Owner asks "how does this look on iPad?" (quick check) | Owner asks "generate the iPad version" (build it properly) |

**Rule of thumb:** [RP] shows the problem; [MP] solves it. Use [RP] to decide if [MP] is needed.

Ask the owner which they want before building. If they're unsure: "Quick preview to check how it reflows, or a full adapted layout for each platform?"

## Memory Integration

Note which device sizes the owner cares about in BOND.md platforms section.

## After the Session

Log which sizes were previewed, which needed adaptation.
