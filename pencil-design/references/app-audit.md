---
name: app-audit
description: Scan existing screens for design inconsistencies, token drift, system violations, and design quality anti-patterns
code: AA
---

# Audit App

Scan all screens in the active .pen file for design inconsistencies — hardcoded values that should be tokens, patterns that deviate from the design system, spacing drift, typography inconsistencies.

**Always load `references/design-knowledge.md`** at the start of every audit. It contains the 25 anti-pattern rules and 15 universal design principles that inform the quality checks below.

## What Success Looks Like

An actionable audit report: exactly what's inconsistent, where, and what to fix. Not a general critique — specific findings the owner can act on.

## Process

1. **Confirm scope:** Before scanning, ask: "Audit all screens in the .pen file, or specific screens?" Large files may take multiple batches.
2. `batch_get` on all top-level frames (full depth)
3. `search_all_unique_properties({properties: ["fill", "fontFamily", "fontSize", "fontWeight", "gap", "padding", "cornerRadius"]})` — surface all unique values
4. Cross-reference against established design tokens from `get_variables` and MEMORY.md
5. Identify deviations

For 5+ screens: announce before spawning — "Scanning {N} screens in parallel — I'll have the audit report shortly." Then spawn subagents to scan in parallel. Each returns compact JSON (max 300 tokens):

```json
{
  "screen": "Dashboard",
  "frame_id": "dashboard-001",
  "hardcoded_colors": ["#F4F4F4", "#EFEFEF"],
  "font_deviations": [],
  "spacing_deviations": [{"property": "gap", "value": 16, "expected": 32}],
  "missing_components": ["SectionHeader appears 3x but not using reusable component"]
}
```

## What to Look For

**Token drift:** Colors that almost match tokens but don't exactly (e.g., #F4F4F4 when the token is #F4F4F5).

**Hardcoded values:** Color/font/spacing values that should reference tokens but are hardcoded.

**Typography inconsistencies:** Font combinations not in the established scale.

**Spacing drift:** Gap and padding values that don't follow the spacing rhythm.

**Component deviations:** Frames that should be component instances but were rebuilt manually.

**Accessibility issues:** Flag obvious contrast problems (use `scripts/contrast-ratio.py` for verification).

### Design Quality Checks (Impeccable-informed)

These checks catch design anti-patterns that token/consistency audits miss. Run them on every audit.

**AI Slop Detection** — Flag these visual anti-patterns that signal generic, undesigned output:

| Pattern | How to detect in .pen | Severity |
|---|---|---|
| Identical card grids | Hash child node structures — if 3+ frames have identical structure + same dimensions, flag | Medium |
| Everything centered | Check top-level content frames: if >80% use `alignItems: "center"`, flag | Low |
| Same spacing everywhere | Collect all gap/padding values — if <3 unique values across 5+ screens, flag as "no rhythm" | Medium |
| Decorative-only elements | Frames with no text children, no interactive purpose, and opacity <0.5 — likely decorative noise | Low |

**Typographic Hierarchy Check** — Verify that the type scale creates clear visual hierarchy:

```
Scan all text nodes → extract fontSize + fontWeight combinations → sort descending

Expected: clear ladder (e.g. 28/800, 24/700, 20/600, 15/400, 13/500, 11/500)
Flag: steps smaller than 2px between adjacent levels (no perceptible difference)
Flag: more than 2 weights used at the same font size (visual noise)
Flag: body text below 14px (readability risk)
Flag: heading weight lighter than body weight (inverted hierarchy)
```

**Cognitive Load Check** — Flag screens with too many competing elements:

```
Per screen frame, count:
  - Interactive elements (buttons, toggles, links, tappable rows): flag if > 7 primary actions
  - Distinct visual sections: flag if > 5 with no progressive disclosure
  - Unique colors used: flag if > 8 (palette bloat)

Report: "Dashboard has 9 primary actions — consider progressive disclosure or grouping"
```

## Output

Present a prioritized audit:
```
Critical (fix before shipping):
  - Dashboard > Header: fill #F4F4F4 should be $surface (#F4F4F5)
  - Settings > Section 3: hardcoded font "Inter" should reference $body

Medium (fix this sprint):
  - Check-in > rows: gap:16 inconsistent (design system: 32 between sections)

Low (nice to have):
  - Onboarding > 3 frames that duplicate SectionHeader component
```

Offer to fix high-priority issues immediately.

## After the Session

Follow the standard session close protocol. Additionally log: audit scope, findings count, what was fixed vs. deferred. Note recurring patterns that suggest design system gaps in MEMORY.md.
