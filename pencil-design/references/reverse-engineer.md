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

### Web App (Chrome DevTools MCP) — Fully Automated

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

### iOS App on Simulator — Fully Automated

**Step 1 — Boot and launch:**

```bash
# List available simulators
xcrun simctl list devices available | grep -E "iPhone|iPad"

# Boot if needed
xcrun simctl boot "iPhone 16 Pro"

# Launch the target app (user provides bundle ID or app name)
xcrun simctl launch booted com.example.app
```

**Step 2 — Guided capture with auto-screenshot:**

Announce: "I'll take screenshots as you navigate. Tell me when you've reached each screen, or I'll capture every 3 seconds if you prefer auto-mode."

```bash
# Single screenshot
xcrun simctl io booted screenshot /tmp/re-capture/screen-001.png

# Or timed burst (auto-mode):
# Take a screenshot every 3 seconds for N seconds
for i in $(seq 1 20); do
  xcrun simctl io booted screenshot "/tmp/re-capture/screen-$(printf '%03d' $i).png"
  sleep 3
done
```

**Step 3 — Deduplicate:**

After auto-capture, compare sequential screenshots to remove duplicates (user was idle on the same screen). Use image comparison:

```bash
# Quick pixel diff — if images are identical or near-identical, skip
python3 -c "
from pathlib import Path
import hashlib
seen = {}
for f in sorted(Path('/tmp/re-capture').glob('*.png')):
    h = hashlib.md5(f.read_bytes()).hexdigest()
    if h in seen: f.unlink()
    else: seen[h] = f
print(f'Kept {len(seen)} unique screens')
"
```

### iOS/iPad Device via AirPlay — Guided

**Setup instructions for the user:**

> 1. Open **QuickTime Player** on your Mac
> 2. File → New Movie Recording
> 3. Click the dropdown arrow next to the record button → select your iPhone/iPad
> 4. Your device screen is now mirrored in QuickTime
> 5. Keep the QuickTime window visible — I'll capture from it

**Or with AirPlay (macOS Monterey+):**

> 1. On your iPhone: open Control Center → Screen Mirroring → select your Mac
> 2. Your phone screen appears in a window on your Mac
> 3. Keep it visible — I'll capture from it

**Guided navigation:**

The system drives the process step by step:

```
"Navigate to the main/home screen and say 'ready'."
→ user says "ready"
→ screencapture -x /tmp/re-capture/01-home.png
→ "Got it. Now open the settings or profile screen."
→ user says "ready"
→ screencapture -x /tmp/re-capture/02-settings.png
→ "Good. Now open any list or detail view."
...
```

**Smart prompting — ask about the app structure first:**

Before capturing, ask: "Describe the main sections of the app — how many tabs, what are the key screens?" This lets the system create a capture plan:

```
Capture plan for [App Name]:
  1. [ ] Tab 1: Dashboard / Home
  2. [ ] Tab 2: History / Feed
  3. [ ] Tab 3: Add / Create
  4. [ ] Tab 4: Profile / Settings
  5. [ ] Key detail screen (from tab 1)
  6. [ ] Any modal / sheet
  7. [ ] Empty state (if accessible)
  8. [ ] Dark mode (if available — toggle in Control Center)
```

Check off each as captured. Announce progress: "4 of 8 screens captured. Next: open the Profile tab."

**Auto-mode option:**

```
"Want me to capture automatically every 3 seconds while you navigate?
Just swipe through the app naturally — I'll sort out the duplicates."
```

Then use `screencapture` in a timed loop, deduplicate after.

### macOS App — Semi-Automated

macOS apps can be captured per-window and inspected via Accessibility APIs.

**Step 1 — Find the app window:**

```bash
# List all windows with their IDs (for targeted capture)
osascript -e 'tell application "System Events" to get {name, id} of every window of every process whose visible is true'

# Or find a specific app:
osascript -e 'tell application "System Events" to get id of every window of process "[App Name]"'
```

**Step 2 — Capture the window:**

```bash
# Capture a specific window by ID (no shadow, no desktop)
screencapture -l <windowID> -o /tmp/re-capture/01-main.png

# Or interactive: let user click the window
screencapture -w -o /tmp/re-capture/01-main.png
```

**Step 3 — Accessibility inspection (optional, powerful):**

macOS Accessibility APIs expose the entire UI tree — labels, roles, frames, values:

```bash
# Dump the accessibility tree of the frontmost app
python3 -c "
import subprocess, json
result = subprocess.run(
    ['osascript', '-e', '''
    tell application \"System Events\"
        set frontApp to first application process whose frontmost is true
        set appName to name of frontApp
        set winList to {}
        repeat with w in windows of frontApp
            set winInfo to {name of w, position of w, size of w}
            set end of winList to winInfo
        end repeat
        return {appName, winList}
    end tell
    '''],
    capture_output=True, text=True
)
print(result.stdout)
"
```

This gives us actual element positions and sizes — more accurate than pixel-guessing for layout extraction.

**Step 4 — Guided navigation for multiple states:**

Mac apps often have multiple view states in one window (sidebar selections, tabs, inspectors). Guide the user:

```
"Click on each sidebar item and say 'ready' — I'll capture each state."
"Open the preferences window and say 'ready'."
"Resize the window to minimum width and say 'ready' — I'll check the compact layout."
```

**Step 5 — Window chrome detection:**

macOS windows have standard chrome (title bar, toolbar, sidebar). Detect:
- **Title bar:** Standard (28px) or tall toolbar style
- **Sidebar:** NavigationSplitView pattern (detect from width ratio)
- **Tab bar:** Segmented control in toolbar or tab view
- **Inspector:** Right-side panel (if window has three columns)

Map these to NavigationSplitView / HSplitView patterns for macOS rebuild.

### Screenshots Folder — Manual

```
"Drop your screenshots in a folder and give me the path.
Name them in order if you can: 01-home.png, 02-settings.png, etc.
Otherwise I'll analyze them in modification-time order."
```

Read all images from the folder, present them back for the user to name/confirm.

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

## Platform-Specific Tips

### Web Apps — Getting the Most Data

- Use `evaluate_script` to extract CSS custom properties (`:root` variables) — these ARE the design tokens
- Check for Tailwind: `evaluate_script` to read `tailwind.config` if it's exposed
- Extract SVG icons and their names for icon mapping
- Check responsive breakpoints: resize viewport and capture at each breakpoint

### iOS Apps — System Conventions

- SF Pro is the system font — don't extract it as a custom font, map to iOS text styles
- Tab bar is 49px, nav bar is 44px (large title: 96px) — use standard heights
- Safe area: 59px top (Dynamic Island), 34px bottom (home indicator)
- Pull-to-refresh, swipe-to-delete — note interaction patterns, not just visuals

### macOS Apps — Window Patterns

- Standard title bar: 28px. Toolbar: 38-52px depending on style
- Sidebar width: typically 200-280px (NavigationSplitView default: 240px)
- Three-column layout: sidebar (240) + content (flexible) + inspector (260-300)
- macOS uses pointer-sized targets (smaller than iOS 44pt minimum)
- Menu bar: not part of the window — capture separately if menu structure matters
- Sheets: slide down from toolbar, not from bottom like iOS
- Popovers: common for settings/options — capture these as separate states
- Use `NSWindow.contentLayoutRect` via Accessibility to get exact content area bounds

### Dark Mode Capture

If the app supports dark mode:

1. Capture all screens in light mode first
2. Switch to dark mode (Settings or Control Center)
3. Re-capture the same screens
4. Extract dark mode tokens as a separate palette
5. Use `[TV]` Theme Variants to set up both themes in Pencil

---

## Memory Integration

After reverse engineering:
- Store the source app name and capture method in session log
- Add extracted design system to BOND.md (this is now the owner's design language)
- Register all created components in `component-registry.md`
- Note which screens were captured and their accuracy scores in MEMORY.md

## After the Session

Log: app name, capture method, screens captured/rebuilt, design system summary, accuracy scores. Update BOND.md with the established design language.
