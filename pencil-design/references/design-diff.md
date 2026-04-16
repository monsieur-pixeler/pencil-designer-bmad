---
name: design-diff
description: Compare two versions of a screen and show exactly what changed
code: DD
---

# Design Diff

Compare two frames — before/after an iteration, two design proposals, or different versions — and produce a clear visual and structural diff.

## What Success Looks Like

A clear answer to "what changed?": screenshots of both versions plus a structured list of additions, removals, and changes. The owner can quickly see the delta and decide if the direction is right.

## Process

1. Read both frames: `batch_get` with `readDepth: 10, resolveVariables: true` on each
2. Screenshot both frames
3. Walk both node trees depth-first, match nodes by `name` property (then by `id` if names aren't unique)
4. Classify changes:

| Change | Detection |
|---|---|
| **Added** | Node in frame B but not frame A |
| **Removed** | Node in frame A but not frame B |
| **Color changed** | Different `fill` value |
| **Typography changed** | Different `fontSize`, `fontWeight`, or `fontFamily` |
| **Spacing changed** | Different `gap`, `padding`, `width`, or `height` |
| **Content changed** | Different text `content` |
| **Moved** | Different position (significant enough to notice) |

## Output

Present side-by-side screenshots with a structured diff:

```
Design Diff: Dashboard v1 → v2

Added:
  + Coach message card (new section below metrics)
  + Notification bell (header, right side)

Removed:
  - Progress ring (was in header)

Changed:
  ~ Header title: fontSize 24→28, fontWeight 600→800
  ~ Metric section: gap 16→24 (more breathing room)
  ~ CTA button: cornerRadius 20→24

Layout impact: +1 section, content shifted down ~80px
```

## Batch Diff

For 5+ screen pairs: announce before spawning — "Diffing {N} screen pairs in parallel — results incoming." Then spawn subagents per pair, each returning compact JSON with change counts. Present summary matrix, drill into specifics on request.

## After the Session

Follow the standard session close protocol. Additionally log: what was compared, what changed, owner's reaction to the diff. Note significant design direction changes in BOND.md.
