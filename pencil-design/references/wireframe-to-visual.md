---
name: wireframe-to-visual
description: Transform Freya's wireframes into polished visual designs in the same .pen file
code: PW
---

# Polish Wireframe

Read an existing wireframe frame, understand its information architecture, and create a polished visual design next to it — in the same .pen file. The wireframe stays untouched as reference. This is the bridge between WDS Phase 4 (Freya's wireframes) and visual implementation.

## What Success Looks Like

Two frames side by side: the wireframe on the left, a pixel-perfect visual design on the right. The owner can see exactly how the wireframe intent was translated into visual design. The polished version is ready for code generation.

## Reading the Wireframe

Use `batch_get({nodeIds: [wireframe-id], readDepth: 10})` to understand the structure. Extract:
- Dimensions and platform (mobile 402px / desktop wider)
- Section hierarchy (what's grouped with what, what's prominent)
- Content inventory (text, images, actions, navigation)
- Priority signal from positioning (top = high priority)

Map wireframe elements to design patterns:
- Large text block at top → Hero metric or Section Header
- Horizontal boxes → Segmented control, metric pair, or tabs
- Vertical stack of similar rows → Grouped list
- Box with text → Card, chat bubble, or notification
- Full-width block at bottom → CTA Button
- Small circle + text → Avatar + profile info
- Horizontal line → Divider

## Creating the Visual Design

1. Find position: `find_empty_space_on_canvas({direction:"right", width:500, height:900, padding:100})`
2. Name convention: if wireframe is "WF — Dashboard", visual is "Dashboard"
3. Build with `placeholder: true`, apply project tokens from DESIGN.md (via `get_variables` or MEMORY.md)
4. Copy chrome from existing screens (status bar, tab bar)
5. Construct sections following the wireframe structure
6. Set `placeholder: false`
7. Screenshot both and present side by side

## Presenting

Show wireframe screenshot (left) + visual design screenshot (right). Include brief interpretation notes: "I read the large box as a coach message card based on the text content. The three horizontal items became a segmented control."

## Batch Processing

**Confirm scope first:** Before starting a batch, present the wireframe list and ask: "Polish all N wireframes, or select specific ones?" Polishing rewrites frames in the .pen file — confirm before proceeding.

For 5+ wireframes, use subagent orchestration — spawn one subagent per wireframe to read structure. Each returns compact JSON (max 300 tokens):

```json
{
  "frame_id": "wf-dashboard",
  "frame_name": "WF — Dashboard",
  "dimensions": {"width": 402, "height": 874},
  "sections": [
    {"type": "metric_display", "content": "Weight metric at top", "priority": "high"},
    {"type": "card", "content": "Coach message area", "priority": "high"},
    {"type": "cta_button", "content": "Full-width action at bottom", "priority": "high"}
  ],
  "chrome": {"has_status_bar": true, "has_tab_bar": true},
  "component_count": 8
}
```

Collect all summaries, then build visual designs sequentially using the JSON.

## After the Session

Follow the standard session close protocol. Additionally log: which wireframes were polished, any interpretation decisions the owner corrected (these reveal visual intent). Update `component-registry.md` for new components.
