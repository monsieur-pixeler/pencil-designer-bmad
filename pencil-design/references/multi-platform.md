---
name: multi-platform
description: Generate iPad, macOS, and web variants from a mobile screen design
code: MP
---

# Multi-Platform Compose

Take a mobile screen and generate adapted variants for other platforms. Not scaling — recomposing. Same content, restructured for each platform's interaction model.

## What Success Looks Like

A row of frames: `[Mobile] [iPad] [macOS] [Web]` with platform labels and screenshots. Each variant is appropriately adapted — not just wider, but restructured for how that platform works.

## Platform Adaptation Rules

| Element | Mobile (402px) | iPad (1024px) | macOS (1440px) | Web (1280px) |
|---|---|---|---|---|
| Navigation | Tab bar (bottom) | Sidebar + tab bar | NavigationSplitView sidebar | Top nav bar |
| Content | Single column | Two-column split | Three-column | Responsive grid |
| Gap between sections | 32px | 40px | 48px | 40px |
| Content padding | 24px | 32px | 40px | max-width container |
| Cards | Full width | Two-column grid | Flexible grid | Responsive grid |
| Touch targets | 44px min | 44px min | Smaller OK (pointer) | Pointer-sized |

## Process

1. Read source frame: `batch_get({nodeIds: [mobile-id], readDepth: 10})`
2. Decompose into content blocks (header, primary, secondary, actions, chrome)
3. For each target platform: find canvas position, create frame, recompose content blocks
4. Apply platform-appropriate dimensions and spacing
5. Screenshot all variants

## Content Block Recomposition

Don't scale — restructure:
- **iPad:** Master-detail split if source has a list. Two-column cards. Tab bar stays but sidebar can be added.
- **macOS:** Always add sidebar navigation. Content gets more horizontal breathing room. Detail panels appear alongside content.
- **Web:** Top nav replaces tab bar. Content in max-width container (centered). CSS Grid for cards.

## Batch Multi-Platform

**Confirm scope first:** Before generating variants, ask: "Generate [Mobile+iPad+macOS+Web] for all N screens, or select specific screens and platforms?" This creates N×4 new frames — confirm scope before proceeding.

For 5+ screens: announce before spawning — "Reading {N} screens in parallel to extract content structure — platform variants incoming." Then spawn subagents to read content structures in parallel. Each returns compact JSON (max 250 tokens):

```json
{
  "screen_name": "Dashboard",
  "frame_id": "dashboard-mobile",
  "content_blocks": ["header", "primary_metrics", "coach_card", "progress_bars", "cta"],
  "nav_type": "tab_bar",
  "card_count": 2,
  "list_count": 0
}
```

Use the summaries to recompose content for each platform variant sequentially.

```
Row 1: Dashboard    — [Mobile] [iPad] [macOS] [Web]
Row 2: Settings     — [Mobile] [iPad] [macOS] [Web]
```

200px vertical gap between rows.

## Memory Integration

Note platform preferences from BOND.md. Log which platforms the owner actually cares about — not everyone needs all four.

## After the Session

Update BOND.md with platform preferences confirmed/changed. Note any recomposition decisions that were unusual.
