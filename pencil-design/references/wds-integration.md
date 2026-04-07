---
name: wds-integration
description: Batch-generate all screens from WDS scenario specs and trigger maps, optionally skipping the wireframe phase
code: WS
---

# Design from WDS

Read WDS spec artifacts and generate complete hi-fi screens — skipping the wireframe phase entirely when a design library is available. This is the bridge between WDS Phase 2 (specs) and development.

## What Success Looks Like

Every scenario screen has a polished visual design in Pencil, verified with screenshots, ready for code generation. The owner has a complete set of screens to approve before any code is written.

## WDS Pipeline

```
Path 1: Specs → Design from WDS → Visual Design → Code
Path 2: Freya Wireframes → Polish Wireframe [PW] → Code
```

If wireframes exist in the .pen file, prefer Path 2. If only specs exist, use Path 1 here.

## Artifact Discovery

Check these paths in order:
1. `{project-root}/design-artifacts/` — Standard WDS structure
2. `{project-root}/_bmad-output/` — BMad Method projects
3. Ask the owner if neither exists

### Standard Structure
```
design-artifacts/
  A-Product-Brief/         → product vision (read for context)
  B-Trigger-Map/           → user psychology, priorities (drives content hierarchy)
  C-UX-Scenarios/          → page specs per screen (PRIMARY INPUT)
    scenario-index.md      → master list of all scenarios
    S01-name/P01-name.md   → individual page specs
  D-Design-System/         → design tokens and component specs
```

## Batch Generation Workflow

### 1. Inventory
Read the scenario index. Present prioritized summary:
```
Found 22 screens across 8 scenarios:
  P1 (Core): Dashboard, Check-in, Program Builder (6 screens)
  P2 (Important): History, Exercises, Calculator (10 screens)
Generate all, or select specific scenarios?
```

### 2. Design System Setup
Before any screens: read DESIGN.md, initialize `set_variables` if needed, load `get_guidelines`.

### 3. Read Page Specs (Subagent Orchestration)
For 5+ page specs: announce before spawning — "Reading {N} screen specs in parallel — I'll start designing as soon as I have the summaries." Then spawn parallel subagents to read specs, each returning compact JSON:
```json
{
  "screen_name": "Dashboard",
  "purpose": "Primary overview with metrics and coach message",
  "sections": [
    {"type": "metric_display", "content": "Weight + start", "priority": "high"},
    {"type": "coach_message", "content": "Weekly AI insight", "priority": "high"},
    {"type": "cta_button", "content": "Start Check-in", "priority": "high"}
  ],
  "navigation": {"tab": "Dashboard", "active": true}
}
```

### 4. Screen Generation
For each screen:
1. `find_empty_space_on_canvas({direction:"right"})` for position
2. Create frame `placeholder: true`
3. Copy chrome from first screen
4. Build sections from spec using patterns in `[DP]`
5. Set `placeholder: false` → screenshot → verify against spec
6. Present for approval

### 5. Component Extraction
After 3+ screens: review for repeating patterns, create reusable components.

## Page Spec → Design Pattern Translation

| Spec Element | Design Pattern |
|---|---|
| Hero metric / KPI | Metric Display |
| Data list | Grouped List with rows |
| Toggle | Row with right-aligned toggle |
| Multi-option | Segmented Control |
| Progress | Progress Bar |
| Coach/AI message | Chat Bubble (received) |
| Navigation tabs | Tab bar with active state |
| Call to action | Full-width CTA Button |

## Memory Integration

Update MEMORY.md with WDS progress after each batch. Note in session log which screens were completed.

## After the Session

Log: screens completed, approval patterns, any spec ambiguities resolved (add to BOND.md workflow preferences).
