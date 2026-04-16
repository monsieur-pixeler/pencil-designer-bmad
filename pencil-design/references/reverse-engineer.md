---
name: reverse-engineer
description: Reverse-engineer any existing app or website into a full Pencil design system — guided capture, visual analysis, token extraction, and pixel-perfect rebuild
code: RE
---

# Reverse Engineer

Take an existing app or website and reverse-engineer it into a complete Pencil design system: capture every screen, extract the design language (colors, typography, spacing, components), and rebuild it all in the .pen canvas with proper tokens.

This is a guided, interactive process. The capture method depends on the source platform.

## What Success Looks Like

A .pen file with every screen of the target app rebuilt as editable Pencil frames, backed by a full design token system (`set_variables`), with reusable components extracted. The owner can now iterate on the design, create variants, or generate code — the app is fully "owned" as a design artifact.

## Source Detection

Ask: **"What are we reverse-engineering?"** Then route:

| Source | Capture Method | Automation Level |
|---|---|---|
| Web app (URL) | Chrome DevTools MCP | Full auto — DOM crawl, CSS extraction, screenshots |
| iOS app on simulator | `xcrun simctl` CLI | Full auto — screenshot CLI, can control navigation |
| iOS/iPad app on device (AirPlay) | `screencapture` on Mac + guided navigation | Semi — user navigates, system captures |
| macOS app | `screencapture` per window + Accessibility inspection | Semi — system captures windows, user navigates between states |
| Android app | User provides screenshots | Manual capture, auto analysis |
| Screenshots folder | Read from disk | Manual capture, auto analysis |
| Figma/Sketch (exported) | User provides PNG/SVG exports | Manual capture, auto analysis |

Also ask: **"What's the goal?"** This determines the output:

| Goal | What Changes |
|---|---|
| **Exact clone** | Rebuild pixel-perfect with the same tokens |
| **Reskin / redesign** | Extract patterns and structure, apply a new design language |
| **Pattern library** | Extract only the component patterns, not full screens |

---

## Phase 1: Capture

Load the capture reference for the detected source:
- Web app → load `references/re-capture-web.md`
- iOS simulator → load `references/re-capture-ios-sim.md`
- iOS device (AirPlay) → load `references/re-capture-ios-device.md`
- macOS app → load `references/re-capture-macos.md`
- Screenshots folder / Figma / Sketch → no capture reference needed — read images from disk

### Screenshots Folder — Manual

```
"Drop your screenshots in a folder and give me the path.
Name them in order if you can: 01-home.png, 02-settings.png, etc.
Otherwise I'll analyze them in modification-time order."
```

Read all images from the folder, present them back for the user to name/confirm.

### Dark Mode Capture

If the app supports dark mode:

1. Capture all screens in light mode first
2. Switch to dark mode (Settings or Control Center)
3. Re-capture the same screens
4. Extract dark mode tokens as a separate palette
5. Use `[TV]` Theme Variants to set up both themes in Pencil

---

## Phase 2: Analyze

After capture, analyze all screenshots. This runs the same way regardless of capture method.

**Announce:** "Analyzing {N} screens — extracting colors, typography, spacing, and component patterns."

### Per-Screen Analysis

For each screenshot, use visual analysis (the LLM reads the image) to extract:

```json
{
  "screen_name": "Dashboard",
  "file": "01-dashboard.png",
  "layout": {
    "type": "vertical_scroll",
    "has_nav_bar": true,
    "has_tab_bar": true,
    "sections": ["header_metrics", "coach_card", "progress_section", "cta"]
  },
  "colors": {
    "background": "#FFFFFF",
    "surface": "#F4F4F5",
    "text_primary": "#18181B",
    "text_secondary": "#71717A",
    "accent": "#F97316"
  },
  "typography": {
    "heading": {"family": "estimated: SF Pro Display", "size": "~28px", "weight": "800"},
    "body": {"family": "estimated: SF Pro Text", "size": "~15px", "weight": "400"},
    "caption": {"family": "estimated: SF Pro Text", "size": "~13px", "weight": "500"}
  },
  "spacing": {
    "section_gap": "~32px",
    "content_padding": "~24px",
    "card_padding": "~16px",
    "card_corner_radius": "~16px"
  },
  "components": ["metric_card", "coach_message_bubble", "progress_bar", "cta_button", "tab_bar", "nav_bar"]
}
```

For **5+ screens**: spawn subagents to analyze in parallel. Announce: "Analyzing {N} screens in parallel — I'll synthesize the design system when all are done." Each returns compact JSON (max 400 tokens).

### Web App Bonus — CSS-Level Precision

When captured via Chrome DevTools, merge the visual analysis with the DOM-extracted CSS values. CSS values are ground truth — visual estimates are fallback only. Flag any discrepancy between visual estimate and CSS reality.

### Cross-Screen Synthesis

After all screens are analyzed, synthesize:

1. **Color palette** — Merge all extracted colors, deduplicate, identify primary/secondary/surface/accent roles
2. **Typography scale** — Merge all font observations into a coherent scale (display, heading, body, caption)
3. **Spacing system** — Find the rhythm (is it 4px? 8px? mixed?)
4. **Component inventory** — Which components appear across multiple screens? (candidates for reusable extraction)
5. **Layout patterns** — Common structural patterns (list screens, detail screens, form screens)

Present the synthesized design system for owner approval before rebuilding:

```
Extracted Design System: [App Name]

Colors:
  Background:     #FFFFFF → $bg
  Surface:        #F4F4F5 → $surface
  Text Primary:   #18181B → $text-primary
  Text Secondary: #71717A → $text-secondary
  Accent:         #F97316 → $accent

Typography:
  Display:  SF Pro Display 28px/800 → $display
  Heading:  SF Pro Display 20px/700 → $heading
  Body:     SF Pro Text 15px/400    → $body
  Caption:  SF Pro Text 13px/500    → $caption

Spacing: 8px grid (gaps: 8, 16, 24, 32)
Corner radius: 16px (cards), 24px (buttons), 8px (small elements)

Components found (3+ instances):
  MetricCard:      8 instances across 4 screens → extract
  SectionHeader:   6 instances across 5 screens → extract
  ListRow:         12 instances across 3 screens → extract
  CTAButton:       4 instances across 4 screens → extract

Approve this system, or adjust before I start building?
```

---

## Phase 3: Rebuild in Pencil

After approval, rebuild every captured screen in the .pen canvas.

### Setup Design Tokens

```
set_variables — create all extracted tokens:
  $bg, $surface, $text-primary, $text-secondary, $accent,
  $display, $body, $heading, $caption,
  spacing values, corner radius values
```

### Rebuild Order

1. **Shared chrome first** — navigation bar, tab bar, status bar (reusable components)
2. **Simplest screen first** — establishes the base patterns
3. **Most complex screen** — proves the system handles edge cases
4. **Remaining screens** — batch-build using established patterns

For each screen:
1. `find_empty_space_on_canvas` for position
2. Create frame at device dimensions (`placeholder: true`)
3. Build section by section, referencing the screenshot for accuracy
4. `placeholder: false` → `get_screenshot` → compare with original
5. Present side-by-side: original screenshot vs. Pencil rebuild

**Announce progress:** "Rebuilding screen 3 of 8: Settings. {estimated time remaining}"

### Accuracy Check

After each screen rebuild, visually compare with the original. Flag differences:

```
Rebuild Accuracy: Dashboard
  ✓ Layout structure matches
  ✓ Color palette matches
  ~ Typography: heading appears 2px larger — adjusted
  ✗ Bottom CTA button: corner radius 20px in original, was 16px — fixed
  Score: 95% match
```

### Component Harvest

After 3+ screens are rebuilt, run `[CH]` Component Harvest to extract reusable components from the rebuilt frames. This turns the one-off rebuild into a proper design system.

---

## Phase 3b: Reskin — Rebuild with a Different Design Language

When the goal is **reskin/redesign**, the rebuild uses the extracted *patterns and structure* but applies a completely different visual identity. This is the "I love how Strong works, but I want it to look like my brand" workflow.

### How Reskin Differs from Clone

| Aspect | Clone | Reskin |
|---|---|---|
| Layout structure | Copy exactly | Copy the patterns (nav, hierarchy, flow) |
| Colors | Extract and match | Replace with owner's palette |
| Typography | Extract and match | Replace with owner's font system |
| Spacing | Extract rhythm | Keep the rhythm, adjust to owner's grid |
| Components | Rebuild identical | Rebuild the concept, style to owner's language |
| Interactions | Document exactly | Document patterns, not specifics |

### Reskin Workflow

**Step 1 — Dual token system:**

After Phase 2 analysis, create TWO token sets:

```
Source tokens (read-only reference):
  $source-bg:           #1C1C1E    (Strong's dark background)
  $source-accent:       #34C759    (Strong's green)
  $source-text-primary: #FFFFFF    (Strong's white text)

Target tokens (owner's design language):
  $bg:                  #FFFFFF    (owner's light background)
  $accent:              #F97316    (owner's orange)
  $text-primary:        #18181B    (owner's dark text)
```

Read target tokens from existing DESIGN.md / BOND.md / Pencil variables. If the owner doesn't have a design system yet, help them create one: "Before I reskin, let's establish your design language. What's your brand palette? Typography preferences?"

**Step 2 — Pattern extraction (not pixel extraction):**

Instead of extracting exact values, extract the *design decisions*:

```
Source Analysis: Strong App

Structural Patterns:
  - Tab bar: 5 tabs, icon + label, bottom-fixed
  - List screens: grouped sections with sticky headers
  - Detail screens: hero metric at top, scrollable content below
  - Cards: rounded corners, subtle elevation, full-width
  - Navigation: push transitions, modal for create/add
  - Empty states: centered illustration + message + CTA

Hierarchy Patterns:
  - Primary numbers: largest text on screen, high contrast
  - Section titles: medium weight, secondary color
  - Body content: system font, standard size
  - Metadata: small, tertiary color, spaced apart

Interaction Patterns:
  - Swipe-to-reveal on list items
  - Pull-to-refresh on main lists
  - Haptic feedback on timer events
  - Rest timer: full-screen modal with large countdown
```

**Step 3 — Rebuild with remapping:**

For each screen, rebuild using the *pattern* but the *owner's tokens*:

```
Original (Strong):                  Reskin (Owner's brand):
- Dark background (#1C1C1E)         → Light background ($bg: #FFFFFF)
- Green accent (#34C759)            → Orange accent ($accent: #F97316)
- SF Pro Display bold metrics       → Owner's display font ($display)
- Tight spacing (12px sections)     → Owner's spacing grid ($section-gap)
- Rounded cards (12px radius)       → Owner's corner radius ($card-radius)
```

Each rebuilt screen gets a side-by-side comparison: original screenshot | reskinned Pencil frame.

**Step 4 — Deviation log:**

Track where the reskin intentionally diverges from the source patterns:

```
Reskin Deviations:
  ✓ Color system: completely replaced (dark → light)
  ✓ Typography: replaced (SF Pro → Outfit + Inter)
  ~ Tab bar: kept 5-tab structure, changed icon style
  ~ Cards: kept layout pattern, increased corner radius (12 → 16px)
  ✗ Rest timer: redesigned as inline component instead of full-screen modal
    (owner preference — logged in BOND.md)
```

This deviation log is valuable for the owner to review: "Here's where I followed their patterns, and here's where I chose differently."

### Reskin with Partial Patterns

Sometimes the owner wants only *some* patterns from the source:

```
"I love Strong's workout tracking flow, but I want my own dashboard and settings."
```

In this case:
1. Capture the full app (all screens)
2. Analyze all screens (full design system extraction)
3. Rebuild only the screens the owner wants (workout flow)
4. Mark remaining screens as "design from scratch" — use the patterns as inspiration, not templates

---

## Phase 4: Design System Export

After all screens are rebuilt:

1. **DESIGN.md generation** — Write a complete `DESIGN.md` from extracted tokens
2. **Component catalog** — Run `[DH]` in docs mode to generate component documentation
3. **Variable sync** — Ensure all Pencil variables match the DESIGN.md
4. **Health check** — Run `[SH]` to verify the new system is internally consistent

Present final summary:

```
Reverse Engineering Complete: [App Name]

Captured:    8 screens (iOS app via AirPlay)
Rebuilt:     8 screens in Pencil
Tokens:      24 design variables created
Components:  6 reusable components extracted
DESIGN.md:   Generated at {project-root}/DESIGN.md

The app is now fully owned as a design artifact.
You can iterate, create variants, or generate code from here.
```

---

## After the Session

Follow the standard session close protocol. Additionally log: app name, capture method, screens captured/rebuilt, design system summary, accuracy scores. Update BOND.md with the established design language.
