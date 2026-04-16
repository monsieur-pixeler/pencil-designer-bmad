---
name: app-map
description: Generate a complete visual screen map of your entire app — inventory all screens, lay them out as a flow grid on canvas, show navigation connections, identify gaps
code: MAP
---

# App Map

The first thing you do before designing a single pixel: map the entire app. Every screen, laid out on one canvas, connected by navigation flows. This is the document-of-truth that keeps the whole project visible and honest.

Works in two directions:
- **Forward:** describe your app → Pencil generates the screen inventory and flow grid
- **Reverse:** hand Pencil a messy .pen file → it maps what exists, finds gaps, and restructures

## What Success Looks Like

A single canvas view where the owner can see every screen in their app, how they connect, and what's missing. Not wireframes — just labeled frames at the right dimensions, arranged in a navigation flow grid. The owner says "yes, that's my app" before a single UI element is designed.

## Forward Map — From Description to Canvas

### Step 1: Screen Inventory

Ask one question: **"Describe your app — what does it do and what are the main sections?"**

From the answer (plus WDS specs if they exist, BOND.md project context, or a Product Brief), generate a screen inventory:

```
Screen Inventory: RippedBody Coach

Core (Tab Bar):
  1. Dashboard        — Primary overview, metrics, coach message
  2. Check-in         — Daily logging (weight, sleep, adherence)
  3. History          — Progress charts and historical data
  4. Program          — Active workout/nutrition program view
  5. Settings         — Preferences, profile, subscription

Flows:
  6. Onboarding (3)   — Welcome → Goal → Setup
  7. Check-in Detail  — Expanded check-in form
  8. Exercise Detail  — Individual exercise in program
  9. Edit Profile     — From Settings

Modals/Sheets:
  10. Quick Log        — Sheet from Dashboard
  11. Coach Message    — Detail view of AI insight

Total: 13 screens (5 tabs + 3 onboarding + 3 detail + 2 modals)
```

**Present for approval:** "This is what I see. Missing anything? Too much?"

### Step 2: Flow Grid Layout

After approval, lay out all screens on the canvas as a visual flow grid.

**Layout principles:**
- **Tab bar screens** in a horizontal row — they're siblings
- **Flows** (onboarding, wizards) in horizontal chains with arrows
- **Detail screens** below their parent — they're children
- **Modals/sheets** offset and slightly overlapping their trigger — they're temporary
- **120px gap** between screens, **200px gap** between groups
- **Flow arrows** connecting screens that navigate to each other

```
Canvas layout (schematic):

[Onboarding 1] ──→ [Onboarding 2] ──→ [Onboarding 3]
                                              │
                                              ▼
┌─────────────────────────────────────────────────────────────┐
│  [Dashboard]    [Check-in]    [History]    [Program]    [Settings]  │
│     │              │                         │              │      │
│  [Quick Log]   [Check-in     [Exercise    [Edit         │      │
│  [Coach Msg]    Detail]       Detail]      Profile]      │      │
└─────────────────────────────────────────────────────────────┘
```

**Building the grid:**

```javascript
// 1. Position all frames
// Use find_empty_space_on_canvas for the first frame, then calculate grid positions

// Tab bar row — 5 screens, 120px gaps
tab1=I("document",{type:"frame",name:"Dashboard",width:402,height:874,fill:"$bg",clip:true,placeholder:true})
tab2=I("document",{type:"frame",name:"Check-in",width:402,height:874,fill:"$bg",clip:true,placeholder:true,x:tab1_x+522})
// ... etc

// Flow arrows — use annotation frames with arrow indicators
arrow=I("document",{type:"frame",name:"→",width:40,height:2,fill:"$text-tertiary"})
// Position between connected screens

// Labels — screen name below each frame
I("document",{type:"text",content:"Dashboard",fontFamily:"$display",fontSize:14,fontWeight:"600",fill:"$text-secondary"})
```

### Step 3: Screen Labels and Flow Annotations

Each frame gets:
- **Name label** below the frame (screen name)
- **Type badge** top-right: `TAB`, `FLOW`, `DETAIL`, `MODAL`, `SHEET`
- **Navigation annotations** between connected screens (thin lines or arrows)

```javascript
// Type badge
badge=I(screen,{type:"frame",cornerRadius:4,fill:"$surface",padding:[2,8],layout:"horizontal"})
I(badge,{type:"text",content:"TAB",fontFamily:"$body",fontSize:9,fontWeight:"700",fill:"$text-secondary",letterSpacing:1})
```

### Step 4: Screenshot the Map

After all frames are placed: `get_screenshot` on the full canvas (or a wrapping frame). Present the overview.

```
"Here's your app map — 13 screens across 4 groups.
All frames are placeholders ready to be designed.

Where do you want to start? I'd suggest the Dashboard —
it sets the design language for everything else."
```

## Reverse Map — From Existing .pen to Flow Grid

### Step 1: Scan What Exists

```
batch_get on all top-level frames → inventory existing screens
search_all_unique_properties({properties: ["name"]}) → get all screen names
```

For 5+ screens: spawn subagents to read structure in parallel. Announce: "Scanning {N} screens to build your app map — one moment." Each returns compact JSON (max 200 tokens):

```json
{
  "frame_id": "abc123",
  "name": "Dashboard",
  "dimensions": "402x874",
  "has_content": true,
  "nav_elements": ["tab_bar", "navigation_bar"],
  "interactive_targets": ["quick_log_button", "coach_card"],
  "child_screens_referenced": ["Quick Log", "Coach Message Detail"]
}
```

### Step 2: Build Navigation Graph

From the screen inventory, reconstruct the navigation graph:
- **Tab bars** → identify sibling screens
- **Navigation bars** with back buttons → identify parent-child relationships
- **Buttons/links** referencing other screens → identify flow connections
- **Sheets/modals** → identify temporary overlays

### Step 3: Gap Analysis

Compare what exists against what a complete app would need:

```
App Map Scan: RippedBody Coach

Screens Found: 9
├── Tab Bar screens: Dashboard, Check-in, History, Program, Settings ✓
├── Detail screens: Check-in Detail, Exercise Detail ✓
├── Modals: Quick Log ✓
└── Flows: Onboarding (1 of 3) ⚠️

Gaps Detected:
  ✗ Onboarding 2 and 3 — referenced in flow but no frames exist
  ✗ Edit Profile — Settings has an "Edit" button but no destination screen
  ✗ Empty states — no empty state variants for any screen
  ✗ Error states — no error state variants

Navigation Issues:
  ⚠ Coach Message card on Dashboard — no detail screen exists
  ⚠ Program screen has "Add Exercise" but no Add Exercise screen

Suggest creating 6 additional screens to complete the app.
```

### Step 4: Reorganize Canvas

If the existing .pen file is disorganized (screens scattered, no logical grouping):

**Confirm before moving:** "Your screens are scattered across the canvas. Want me to reorganize them into a flow grid?"

If approved:
1. Calculate new positions following the grid layout principles
2. Move all frames to their new positions: `batch_design` with move operations
3. Add flow arrows and labels
4. Screenshot the reorganized map

## Map Modes

### Full Map
All screens at actual device dimensions. Good for up to ~15 screens. Beyond that, use Thumbnail Map.

### Thumbnail Map
All screens at 25% scale in a compact overview grid. Good for 15-50 screens. Each thumbnail is still clickable for detail.

```javascript
// Thumbnail version — 100x218 per screen (25% of 402x874)
thumb=I("document",{type:"frame",name:"Dashboard (thumb)",width:100,height:218,fill:"$bg",clip:true,placeholder:true})
```

### Section Map
Group screens by section/tab and create a map per section. Good for very large apps (50+ screens).

## Ongoing Map Maintenance

After every Create session where new screens are built:
- Check if the new screen is on the map
- If not, add it to the appropriate position
- Update flow arrows
- Note in session log: "App Map updated: added {screen name} to {section}"

After every Validate session:
- Check if the map matches reality (no orphaned frames, no missing screens)
- Flag discrepancies

## Integration with Other Capabilities

| Triggered from | What happens |
|---|---|
| [WS] WDS Integration | After batch-generating screens from specs, auto-update the map |
| [RE] Reverse Engineer | After rebuild, generate map from the rebuilt screens |
| [ID] Import Design | After analysis, generate map from existing screens |
| [CH] Component Harvest | Map highlights which screens share components |
| [AA] App Audit | Map shows which screens have audit findings (color-coded) |
| [SH] Design System Health | Map shows health status per screen |

## Starting the Design Flow

After the map is approved, the owner picks where to start. Pencil suggests a starting point based on:

1. **Highest-impact screen first** — usually the main tab (Dashboard)
2. **Design system driver** — the screen that establishes the most patterns
3. **Owner's priority** — what they're most excited about

Then: load `[DP]` Design & Polish for the selected screen. The map stays on canvas as the reference — every new screen fills in a placeholder frame.

## After the Session

Follow the standard session close protocol. Additionally log: screens inventoried, map layout chosen, gaps identified, which screen was picked to start designing. Store the screen inventory (count, names, status) in MEMORY.md.
