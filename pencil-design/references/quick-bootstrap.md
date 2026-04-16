---
name: quick-bootstrap
description: Full pipeline bootstrap — from nothing (or brownfield) to all screens on canvas in 5 minutes, orchestrating WDS agents, design setup, and optional code handoff
code: QB
---

# Quick Bootstrap

The fastest path from "I have an idea" or "I have a messy app" to "all screens designed on canvas." Orchestrates the full agent pipeline: analysis, specs, wireframes, design system, screen map, visual design — and optionally hands off to code implementation.

## What Success Looks Like

Within 5 minutes: a complete Pencil canvas with every screen of the app as a frame in a flow grid, backed by a proper design token system. The owner can immediately start iterating on any screen.

For brownfield apps: the existing running app is captured, analyzed, mapped, and ready for redesign — all in one flow.

## Source Detection (Auto-Scan)

Before asking any questions, scan the project for what already exists. Run all checks in parallel:

```
Parallel scan (< 30 seconds):

├─ Source code?
│   ├─ .xcodeproj / .xcworkspace → iOS/macOS app exists
│   ├─ package.json / src/ → React/web app exists
│   └─ Neither → greenfield
│
├─ WDS artifacts?
│   ├─ design-artifacts/A-Product-Brief/ → product context available
│   ├─ design-artifacts/B-Trigger-Map/ → user psychology mapped
│   ├─ design-artifacts/C-UX-Scenarios/ → screen specs available
│   └─ _bmad-output/C-UX-Scenarios/ → BMad project specs
│
├─ Design files?
│   ├─ *.pen files → existing Pencil designs
│   ├─ DESIGN.md → design system documented
│   └─ design-artifacts/D-Design-System/ → WDS design system
│
├─ Running app?
│   ├─ Simulator booted? → xcrun simctl list devices booted
│   └─ Dev server running? → check localhost:3000/5173/8080
│
└─ Available agents?
    ├─ wds-agent-freya-ux → UX designer available
    ├─ wds-agent-saga-analyst → business analyst available
    ├─ bmad-agent-architect (Winston) → architect available
    ├─ bmad-agent-dev (Amelia) → developer available
    ├─ bmad-quick-dev → quick implementation available
    └─ wds-5-agentic-development → agentic dev pipeline available
```

## Present Scan Results

Show everything found in one compact overview:

```
Quick Bootstrap Scan: RippedBody Coach

Source Code:     ✓ SwiftUI app (RippedBodyCoach.xcodeproj)
                 ✓ React/Tauri app (package.json + src/)
WDS Artifacts:   ✓ Product Brief found
                 ✓ Trigger Maps (12 scenarios)
                 ✓ UX Scenarios (22 screens across 8 scenarios)
Design System:   ✓ DESIGN.md found (Gentle Power identity)
                 ✗ No .pen file yet
Running App:     ✗ No simulator booted
Available Agents: ✓ Freya (UX), ✓ Saga (analyst), ✓ Amelia (dev)

Recommended path: Foundation → Map → Create (WDS batch)
You have everything needed — let's go straight to design.
```

Or for a greenfield:

```
Quick Bootstrap Scan: New Project

Source Code:     ✗ None
WDS Artifacts:   ✗ None
Design System:   ✗ None
Running App:     ✗ None
Available Agents: ✓ Freya, ✓ Saga, ✓ Amelia

Recommended path: You have no specs yet.
Option A: I'll start Saga for a product brief → Freya for UX scenarios → then I design
Option B: Describe your app and I'll map + design directly (faster, less structured)
```

## Pipeline Routes

Based on what's found, route to the optimal pipeline:

### Route 1: Greenfield — Nothing Exists

```
[No specs, no code, no design]

Step 1: "Describe your app in 2-3 sentences"
Step 2: Choose path:

Path A (Full WDS — 30 min, thorough):
  → Saga: Product Brief (5 min)
  → Freya: Trigger Map → Scenarios → Wireframes (15 min)
  → Pencil: [DS] tokens → [MAP] flow grid → [DP] visual design (10 min)

Path B (Quick Design — 5 min, fast):
  → Pencil: [DS] propose design system from description
  → Pencil: [MAP] generate screen inventory + flow grid
  → Pencil: [DP] start designing the first screen
  → (WDS specs can be added retroactively)
```

**For Path A, orchestrate the agents:**

1. If Saga is available: "Let me get Saga to draft a quick product brief. This gives us context for design decisions."
   - Invoke: `/wds-agent-saga-analyst` with the app description
   - Capture: product brief summary (target user, core value, key differentiators)

2. If Freya is available: "Now Freya will map the user experience."
   - Invoke: `/wds-agent-freya-ux` with product brief context
   - Capture: scenario list with screen inventory
   - If Freya produces wireframes in .pen: those become our starting point for [PW]

3. Return to Pencil: with scenarios and optional wireframes
   - [DS] — set up design tokens
   - [MAP] — lay out all screens from scenario inventory
   - [DP] or [WS] — start designing (batch from specs, or screen-by-screen)

### Route 2: Has WDS Specs — No Design Yet

```
[Specs exist, no .pen file]

→ Pencil: [DS] read DESIGN.md or create tokens
→ Pencil: [MAP] generate flow grid from scenario-index.md
→ Pencil: [WS] batch-generate all screens from specs
→ Done in ~5 minutes for 10-15 screens
```

### Route 3: Brownfield — Running App, No Design Files

```
[Code exists, app runs, no .pen or DESIGN.md]

Step 1: Capture the running app
  ├─ Simulator booted? → xcrun simctl screenshot (auto, all screens)
  ├─ Dev server? → Chrome DevTools MCP (auto, all routes)
  └─ Neither? → "Boot the simulator / start the dev server and I'll capture"

Step 2: Analyze captures
  → Extract tokens (colors, typography, spacing)
  → Identify all screens and navigation flows
  → Detect components and patterns

Step 3: Bootstrap in Pencil
  → [DS] import extracted tokens
  → [MAP] build flow grid from captured screens
  → All frames are now on canvas, backed by proper tokens
  → Ready for iteration / redesign

Optional: scan source code for existing token definitions
  → Swift: DesignSystem/ColorTokens.swift, Typography.swift
  → React: globals.css, tailwind.config.*, design-tokens.css
  → Cross-reference with visual extraction for accuracy
```

### Route 4: Brownfield — Spaghetti Design

```
[.pen file exists but it's a mess]

Step 1: Diagnose (3-layer scan)
  → Design layer: token drift, hardcoded values, inconsistencies
  → Structure layer: wireframes exist? specs exist? DESIGN.md?
  → Documentation layer: component registry? scenario specs matching screens?

Step 2: Triage
  → "Your design has 14 unique colors (should be 6), spacing is inconsistent,
     and 4 screens don't match their WDS specs. Here's my cleanup plan:"

Step 3: Execute
  → [DS] cleanup mode — consolidate tokens
  → [MAP] reverse mode — reorganize canvas into flow grid
  → [AA] audit — verify consistency after cleanup
  → [CH] harvest — extract components from cleaned screens
```

### Route 5: Platform Migration

```
[React app exists, switching to SwiftUI]

Step 1: Capture existing React app (Chrome DevTools)
  → Extract all CSS tokens, screenshots, component patterns

Step 2: Transform tokens
  → CSS variables → SwiftUI DesignSystem tokens
  → Tailwind classes → SwiftUI modifiers (via [GC] translation table)
  → React components → SwiftUI view patterns

Step 3: Rebuild
  → [DS] with SwiftUI-native tokens
  → [MAP] same screen inventory, new platform annotations
  → [DP] rebuild screens with SwiftUI-native patterns
     (NavigationStack, List(.insetGrouped), TabView)

Step 4: Optional handoff to Amelia
  → "Screens are designed. Want me to get Amelia to implement these in SwiftUI?"
  → Invoke: bmad-agent-dev or bmad-quick-dev with design specs + generated code
```

## Agent Orchestration Protocol

When invoking other agents, follow this protocol:

### Pre-Flight Check

Before suggesting any agent, verify it exists:

```
Check skill availability:
  1. Look for the skill in available skills list
  2. If not found: skip the suggestion entirely — don't mention unavailable agents
  3. If found: present as an option, never force
```

### Handoff Format

When handing off to another agent, provide structured context:

**To Saga (product brief):**
```
"The owner is building [app description]. They need a quick product brief
to inform design decisions. Focus on: target user, core value proposition,
key differentiators, and primary use cases. Keep it concise — this feeds
into UX design and visual design next."
```

**To Freya (UX design):**
```
"We're bootstrapping [app name]. Product context: [brief from Saga or owner].
The owner needs: scenario outlines with screen inventory, and optionally
wireframes in .pen. Pencil will use the scenario list for the app map
and the wireframes (if created) as starting points for visual design."
```

**To Amelia / Quick-Dev (implementation):**
```
"Pencil has designed [N] screens for [app name] in [framework].
Design tokens: [DESIGN.md path]
Generated code: [code from [GC] or export path]
The owner wants these implemented. Start with [screen name].
Design files: [.pen file path]"
```

### Progress Announcements

Keep the owner informed throughout the pipeline:

```
"Quick Bootstrap: RippedBody Coach

[✓] Scan complete — SwiftUI app found, WDS specs available
[✓] Design system imported from DESIGN.md (6 colors, 2 fonts, 8px grid)
[▶] Building app map from 22 scenario specs...
[ ] Visual design (batch)
[ ] Ready for iteration

Step 3 of 5 — mapping 22 screens onto canvas"
```

## Code Handoff — The Last Mile

After design is complete, offer the code pipeline:

```
"All 15 screens are designed and on canvas.

What's next?
[1] Generate code — I'll create SwiftUI/React code from the designs [GC]
[2] Hand off to dev — I'll brief Amelia to implement these screens
[3] Export — PNG exports + component docs for manual implementation [DH]
[4] Keep designing — iterate on specific screens first

For [1] or [2], I'll include the design tokens, component hierarchy,
and any animation specs in the handoff."
```

If the owner chooses code handoff and a dev agent is available:

1. Run [GC] on priority screens → generate code
2. Package: design tokens + generated code + screen screenshots
3. Invoke dev agent with the package
4. Report: "Amelia is implementing Dashboard, Check-in, and Settings. I'll stay available for design questions."

## After the Session

Follow the standard session close protocol. Additionally log: bootstrap route taken, scan results, agents orchestrated, screens generated, time to canvas. Store screen inventory in MEMORY.md. Note agent output quality in BOND.md.
