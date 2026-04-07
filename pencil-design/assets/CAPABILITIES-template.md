> **Note for init-sanctum.py:** This file is a reference example only. The init script generates `CAPABILITIES.md` dynamically from capability frontmatter — this template is never copied directly. Keep it up to date as a human-readable reference, but do not use it as the authoritative source of truth for scaffolding.

# Capabilities

## Built-in

| Code | Name | Description | Source |
|------|------|-------------|--------|
| [DP] | pencil-patterns | Design screens, components, and iterate on existing designs in Pencil canvas | `references/pencil-patterns.md` |
| [PW] | wireframe-to-visual | Transform Freya's wireframes into polished visual designs in the same .pen file | `references/wireframe-to-visual.md` |
| [WS] | wds-integration | Batch-generate all screens from WDS scenario specs and trigger maps, optionally skipping the wireframe phase | `references/wds-integration.md` |
| [GC] | design-to-code | Generate production code from Pencil designs, or recreate existing code as Pencil designs | `references/design-to-code.md` |
| [TV] | theme-variants | Generate light/dark mode variants or alternative color schemes side by side | `references/theme-variants.md` |
| [MP] | multi-platform | Generate iPad, macOS, and web variants from a mobile screen design | `references/multi-platform.md` |
| [ID] | import-design | Analyze existing Pencil designs to extract patterns, tokens, and component opportunities | `references/import-design.md` |
| [CH] | component-harvest | Extract reusable components from existing screens and register them in the design system | `references/component-harvest.md` |
| [DH] | design-handoff | Export screens for development and auto-generate component library documentation | `references/design-handoff.md` |
| [AA] | app-audit | Scan existing screens for design inconsistencies, token drift, and system violations | `references/app-audit.md` |
| [DD] | design-diff | Compare two versions of a screen and show exactly what changed | `references/design-diff.md` |
| [AC] | accessibility-check | WCAG audit on Pencil designs before code — contrast, touch targets, readability | `references/accessibility-check.md` |
| [SH] | design-system-health | Automated health check comparing design tokens with code tokens, measuring component reuse, detecting drift | `references/design-system-health.md` |
| [RP] | responsive-preview | Preview a screen at multiple device sizes to verify responsive behavior | `references/responsive-preview.md` |
| [MV] | marketing-visual | Design landing pages and marketing visuals — orchestrates with marketing/storytelling agents for content | `references/marketing-visual.md` |
| [FM] | framer-motion | Specify animations and transitions for Pencil designs, generate Framer Motion React code | `references/framer-motion.md` |
| [SA] | swiftui-animations | Specify animations and transitions for Pencil designs, generate SwiftUI modifier chains | `references/swiftui-animations.md` |

## Learned

_Capabilities added by the owner over time. Prompts live in `capabilities/`._

| Code | Name | Description | Source | Added |
|------|------|-------------|--------|-------|

## Capability Selection Guide

When multiple capabilities could apply, use this order:

| Situation | Start with |
|---|---|
| Creating new screens or components | `[DP]` pencil-patterns |
| Polishing Freya wireframes | `[PW]` wireframe-to-visual |
| Generating all screens from WDS specs | `[WS]` wds-integration |
| Checking token drift or system violations | `[SH]` design-system-health |
| Auditing existing screens for inconsistencies | `[AA]` app-audit |
| Analyzing an unknown .pen file for the first time | `[ID]` import-design |
| Exporting or documenting for developers | `[DH]` design-handoff |

**[ID] vs [AA] vs [SH] — when to use which:**
- `[ID]` — first analysis of an unfamiliar file; extracts what's there and names it
- `[AA]` — ongoing audit of known screens; flags deviations from established system
- `[SH]` — automated health check comparing Pencil against code; runs in Pulse

## How to Add a Capability

Tell me "I want you to be able to do X" and we'll create it together.
I'll write the prompt, save it to `capabilities/`, and register it here.
Next session, I'll know how.
Load `references/capability-authoring.md` for the full creation framework.

## Tools

### Pencil MCP (primary)

Connected via VS Code Extension or Desktop App. Core tools:

| Tool | Purpose |
|------|---------|
| `batch_design` | Create/update/copy/replace/move/delete nodes (max 25 ops per call) |
| `get_screenshot` | Visual verification of frames |
| `get_variables` / `set_variables` | Read and write design tokens |
| `batch_get` | Read nodes, search patterns, discover components |
| `get_guidelines` | Load Pencil style guides |
| `find_empty_space_on_canvas` | Position new frames |
| `snapshot_layout` | Check layout structure for issues |
| `export_nodes` | Export frames as PNG/JPEG/WEBP/PDF |
| `open_document` | Open or create .pen files |
| `search_all_unique_properties` | Find all unique property values across frames |
| `replace_all_matching_properties` | Bulk update matching property values |

### User-Provided Tools

_Additional MCP servers or services the owner has made available. Document them here._
