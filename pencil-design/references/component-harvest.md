---
name: component-harvest
description: Extract reusable components from existing screens and register them in the design system
code: CH
---

# Component Harvest

Scan existing screens for recurring patterns and extract them as reusable components (`reusable: true`). Grows the design system through use rather than upfront planning.

## What Success Looks Like

A set of named, reusable components registered in `component-registry.md`. Future screens can use instances (`type: "ref"`) instead of rebuilding the same structure. The design system grows from actual usage.

## When to Harvest

Proactively suggest during design sessions when:
- The same pattern appears 3+ times across screens
- A complex structure is being rebuilt manually
- The owner is clearly copying elements between frames

Explicitly on request: "harvest components" or "extract components from these screens".

## Process

1. `batch_get` with full depth on all screens (or selected frames)
2. For 5+ screens: announce before spawning — "Scanning {N} screens for recurring patterns — this will take a moment." Then spawn subagents to analyze in parallel. Each returns compact JSON (max 200 tokens):

```json
{
  "screen": "Dashboard",
  "frame_id": "dashboard-001",
  "patterns": [
    {"type": "section_header", "count": 3, "node_ids": ["hdr-1", "hdr-2", "hdr-3"]},
    {"type": "metric_row", "count": 2, "node_ids": ["row-4", "row-5"]}
  ]
}
```

3. Aggregate across all screens, group by pattern type
4. **Confirm before extracting:** Present candidates with usage counts and ask which to extract:
   ```
   Section Header: 8 instances across 6 screens → create component? [Y/n]
   Metric Row: 5 instances → create component? [Y/n]
   ```
5. For approved candidates: create `reusable: true` nodes, replace instances with `type: "ref"`
6. Update `component-registry.md`

## Component Creation

```javascript
// Extract a section header as reusable component:
comp=I("document",{type:"frame",name:"SectionHeader",reusable:true,...same-props})
// Replace first instance:
R("original-node-id", {type:"ref", ref:comp})
// Replace remaining instances:
// (use replace_all_matching_properties for consistent replacements)
```

## Registry Entry

After creating each component:
```markdown
| SectionHeader | node-id | Title + counter row | Dashboard, Check-in, Settings |
```

## After the Session

Follow the standard session close protocol. Additionally log: which patterns were harvested, which were deferred, component granularity preferences. Update `component-registry.md` after every harvest.
