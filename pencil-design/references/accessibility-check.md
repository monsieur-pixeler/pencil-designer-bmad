---
name: accessibility-check
description: WCAG and iOS/HIG audit on Pencil designs before code — contrast, touch targets, readability, safe area, text styles
code: AC
---

# Accessibility Pre-Check

Catch accessibility failures at design time. Fixing in Pencil is minutes; fixing in shipped code is hours.

## What Success Looks Like

A per-screen accessibility report with pass/fail for contrast, touch targets, and readability. Specific failures with suggested fixes. The owner can fix issues in the design before code is written.

## Checks

### Contrast Ratios

Run `scripts/contrast-ratio.py` for every text/background pair:

```bash
python3 scripts/contrast-ratio.py --fg "#000000" --bg "#FFFFFF"
```

Requirements:
- Body text on background: 4.5:1 (AA minimum)
- Large text (≥18px or ≥14px bold): 3:1 (AA)
- Text on surface cards: 4.5:1 (AA)
- Border/divider: 3:1 (non-text contrast)

### Touch Targets

Read interactive elements (buttons, rows with chevrons, pills, toggles, icons):
- Buttons: 44×44px minimum
- List rows: 44px height minimum
- Icon buttons: 44×44px (including padding/hit area)

### Text Readability

- Minimum body text: 11px
- Recommended body: 14px+
- Line height for body text: 1.3× minimum

### Color-Only Information

Flag elements where color is the sole differentiator:
- Active/inactive tabs only by color → add weight change
- Success/error only by red/green → add icon or label

### iOS / HIG Compliance (SwiftUI projects)

Run these checks when the code framework is SwiftUI or the project targets iOS/iPadOS:

**Safe area clearance:**
- Content must not render behind the Dynamic Island on iPhone 14 Pro and later (top safe area inset: 59px on 14 Pro, 61px on 15 Pro)
- Bottom content must clear the home indicator (34px on full-screen, 21px with tab bar)
- Flag frames where interactive elements sit within 8px of the safe area edge

**Navigation and tab bar heights:**
- Standard tab bar height: 49px (83px with home indicator padding on modern devices)
- Navigation bar height: 44px (standard), 96px (large title)
- Flag content that overlaps these zones

**iOS text style minimums:**
- Caption 2 (iOS minimum): 11px / SF Pro — flag anything below this
- Body (recommended minimum for reading): 17px / SF Pro
- Avoid custom fonts below 12px in any secondary context

**Dynamic Type readiness:**
- Flag fixed font sizes that don't use iOS text styles ($caption, $body, $headline, etc.)
- Prefer SF Pro / System font tokens over hardcoded sizes

**Touch target compliance (iOS-specific):**
- Apple HIG minimum: 44×44pt (same as WCAG, but applies to ALL interactive elements including nav bar items)
- Tab bar icons: 25×25pt image, 44pt touch area
- Navigation bar back button: full 44pt height

```
iOS / HIG Compliance: Dashboard

Safe Area:
  ✓ Content starts below Dynamic Island (gap: 72px)
  ✗ Bottom CTA overlaps home indicator — lift by 34px

Tab Bar:
  ✓ Tab bar height: 49px (correct)
  ✗ Active tab uses color-only indicator — add fill or weight change

Text Styles:
  ✗ Caption text: 10px — below iOS minimum (11px)
    → Use $caption2 token (11px)
```

## Output

```
Accessibility Check: Dashboard

Contrast:
  ✓ Primary text on background: 21:1 — AAA
  ✗ Hint text (#A1A) on surface (#F4F): 2.4:1 — FAIL
    → Fix: darken to #71717A

Touch Targets:
  ✓ CTA button: 354×56px
  ✗ Rating pills: 32×32px — FAIL (need 44×44)
    → Fix: increase or add padding frame

Score: 8/12 pass, 2 fail
```

## Batch Check

**Confirm scope first:** Ask: "Check all screens or specific screens?" before starting a full audit.

For 5+ screens: announce before spawning — "Running accessibility audit on {N} screens in parallel — I'll report all findings together." Then spawn subagents per screen. Each returns compact JSON (max 250 tokens):

```json
{
  "screen": "Dashboard",
  "frame_id": "dashboard-001",
  "contrast_pairs": [
    {"fg": "#71717A", "bg": "#F4F4F5", "ratio": 2.4, "passes_aa": false, "context": "hint text on surface"}
  ],
  "touch_targets_failing": [
    {"element": "Rating pill", "size": "32x32", "minimum": "44x44"}
  ],
  "text_issues": [],
  "color_only_issues": []
}
```

Present summary matrix, drill into specifics on request.

## Memory Integration

Note recurring accessibility issues in session log. If systematic (e.g., all cards use substandard hint text), note in MEMORY.md for future designs.

## After the Session

Log: screens audited, failures found, what was fixed.
