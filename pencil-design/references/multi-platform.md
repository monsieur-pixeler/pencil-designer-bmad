---
name: multi-platform
description: Generate iPad, macOS, and web variants from a mobile screen design — includes quick preview mode for size checks
code: MP
aliases: [RP]
---

# Multi-Platform Compose

Take a mobile screen and generate adapted variants for other platforms. Not scaling — recomposing. Same content, restructured for each platform's interaction model.

## Mode Selection

Ask before starting: **"Quick preview to check how it reflows, or full adapted layouts for each platform?"**

- **Preview mode** (legacy `[RP]`): Same layout at different device sizes — shows overflow, clipping, reflow. Fast sanity check. See [Preview Mode](#preview-mode) below.
- **Full mode**: Content restructured per platform (sidebar, multi-column, pointer targets). Proper adaptation. See the rest of this document.

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

---

## Preview Mode

Quick visual check: same layout at different device sizes. No recomposition — just shows overflow, clipping, and reflow behavior. Use this to decide if full adaptation is needed.

### Standard Device Sizes

| Device | Width | Height |
|---|---|---|
| iPhone SE | 375px | 667px |
| iPhone 15 | 393px | 852px |
| iPhone 15 Plus | 430px | 932px |
| iPad Air | 820px | 1180px |
| iPad Pro 13" | 1024px | 1366px |
| MacBook 13" | 1280px | 800px |
| MacBook Pro 16" | 1440px | 900px |

### Preview Process

1. Read source frame and batch all canvas position queries before creating any frames:
   - `batch_get({nodeIds: [id], readDepth: 5})` — read source frame structure
   - In one batch: call `find_empty_space_on_canvas` for each target size position
2. Create all target frames from the pre-fetched positions
3. Copy the layout as-is to each frame (different dimensions only)
4. Screenshot all frames in a single batch
5. Present as a comparison row with device labels

### Preview Output

```
Preview: Dashboard

[iPhone SE — 375px] [iPhone 15 — 393px] [iPad Air — 820px] [MacBook 13" — 1280px]
   ↑ content clips      ↑ fits well          ↑ lots of space     ↑ needs sidebar
```

**After preview:** "Want me to create full adapted layouts for the sizes that need it? That's full [MP] mode."

---

## Memory Integration

Note platform preferences from BOND.md. Log which platforms the owner actually cares about — not everyone needs all four. In preview mode, note which device sizes the owner checks regularly.

## After the Session

Update BOND.md with platform preferences confirmed/changed. Note any recomposition decisions that were unusual. For preview mode, log which sizes were previewed and which needed full adaptation.
