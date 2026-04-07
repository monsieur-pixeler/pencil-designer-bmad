---
name: app-audit
description: Scan existing screens for design inconsistencies, token drift, and system violations
code: AA
---

# Audit App

Scan all screens in the active .pen file for design inconsistencies — hardcoded values that should be tokens, patterns that deviate from the design system, spacing drift, typography inconsistencies.

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

## Memory Integration

Note major findings in session log. If recurring patterns suggest a design system gap, add to MEMORY.md.

## After the Session

Log: audit scope, findings count, what was fixed vs. deferred.
