> **Note for init-sanctum.py:** This file is a reference example only. The init script generates `CAPABILITIES.md` dynamically from capability frontmatter — this template is never copied directly. Keep it up to date as a human-readable reference, but do not use it as the authoritative source of truth for scaffolding.

# Capabilities

## Built-in

| Code | Name | Description | Source |
|------|------|-------------|--------|
| [MAP] | app-map | Generate a complete visual screen map of your entire app — inventory, flow grid, navigation connections, gap analysis | `references/app-map.md` |
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
| [DS] | design-system-setup | Interactively set up, import, or consolidate a design system — tokens, palette, typography, DESIGN.md | `references/design-system-setup.md` |
| [MV] | marketing-visual | Design landing pages and marketing visuals — orchestrates with marketing/storytelling agents for content | `references/marketing-visual.md` |
| [AN] | animate | Specify animations and transitions — auto-detects framework (SwiftUI or Framer Motion) from BOND.md | `references/animate.md` |
| [RE] | reverse-engineer | Reverse-engineer any existing app or website into a full Pencil design system — guided capture, analysis, and pixel-perfect rebuild | `references/reverse-engineer.md` |
| [QB] | quick-bootstrap | Full pipeline bootstrap — from nothing or brownfield to all screens on canvas in 5 minutes, orchestrating available agents | `references/quick-bootstrap.md` |

### Legacy Aliases (still work, redirect to merged capabilities)

| Legacy Code | Redirects To | Mode |
|---|---|---|
| [FM] | [AN] Animate | Framer Motion — loads `references/animate-framer-motion.md` |
| [SA] | [AN] Animate | SwiftUI — loads `references/animate-swiftui.md` |
| [RP] | [MP] Multi-Platform | Preview mode — quick size check without recomposition |

## Learned

_Capabilities added by the owner over time. Prompts live in `capabilities/`._

| Code | Name | Description | Source | Added |
|------|------|-------------|--------|-------|

## Capability Selection Guide

### Design Phases

Capabilities are grouped into phases. You don't have to follow them in order — jump to wherever you need. But for a new project, this is the natural flow:

```
Discover → Foundation → Map → Create → Refine → Validate → Deliver
                                                              ↑
                                                    Maintain (always)
```

| Phase | When | Capabilities |
|---|---|---|
| **Discover** | Understanding what exists | `[RE]` reverse-engineer, `[ID]` import-design |
| **Foundation** | Setting up the design system | `[DS]` design-system-setup |
| **Map** | Planning the whole app | `[MAP]` app-map |
| **Create** | Building screens | `[DP]` design, `[PW]` wireframe→visual, `[WS]` from WDS specs, `[MV]` marketing |
| **Refine** | Variants and animations | `[TV]` themes, `[MP]` multi-platform, `[AN]` animate |
| **Validate** | Quality checks | `[AC]` accessibility, `[AA]` audit, `[DD]` diff, `[CH]` component harvest |
| **Deliver** | Handoff to development | `[GC]` code generation, `[DH]` handoff + docs |
| **Maintain** | Ongoing health | `[SH]` design system health (Pulse) |

### Quick Routing

| Situation | Start with |
|---|---|
| Starting from scratch or existing app | `[QB]` quick-bootstrap → auto-detects what exists, orchestrates the full pipeline |
| Starting a new app (manual) | `[MAP]` app-map → see all screens before designing any |
| Creating screens or components | `[DP]` pencil-patterns |
| Polishing Freya wireframes | `[PW]` wireframe-to-visual |
| Generating screens from WDS specs | `[WS]` wds-integration |
| Reverse-engineering an existing app | `[RE]` reverse-engineer |
| Analyzing an existing .pen file | `[ID]` import-design |
| Design is a mess — need cleanup | `[ID]` analyse → `[MAP]` reorganize → `[AA]` audit |
| Checking token drift | `[SH]` design-system-health |
| Exporting for developers | `[DH]` design-handoff |

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

### Ecosystem Agents (Orchestration Partners)

Pencil can orchestrate with these agents when they're installed. Always check availability before suggesting — never reference an agent that isn't installed.

| Agent | Skill | Role in Pipeline | Pencil Handoff |
|---|---|---|---|
| **Saga** | `wds-agent-saga-analyst` | Product brief, market research | Pencil receives product context for design decisions |
| **Freya** | `wds-agent-freya-ux` | Trigger maps, scenarios, wireframes | Pencil receives scenario list for [MAP] and wireframes for [PW] |
| **Winston** | `bmad-agent-architect` | Architecture decisions | Pencil receives technical constraints (framework, platform) |
| **Amelia** | `bmad-agent-dev` | Story-based code implementation | Pencil sends design specs + generated code via [GC] |
| **Quick-Dev** | `bmad-quick-dev` | Rapid code implementation | Pencil sends generated code for quick builds |

**WDS Pipeline Skills** (if installed):
| Skill | Phase | Pencil Uses |
|---|---|---|
| `wds-1-project-brief` | Product Brief | Context for design decisions |
| `wds-2-trigger-mapping` | Trigger Maps | User psychology → content hierarchy |
| `wds-3-scenarios` | Scenario Outlines | Screen inventory for [MAP] |
| `wds-4-ux-design` | UX Specs + Wireframes | Page specs for [WS], wireframes for [PW] |
| `wds-5-agentic-development` | Code Implementation | Receives [GC] output for build |

**Design Quality Partners** (if installed):
| Skill | Role | Integration |
|---|---|---|
| `teach-impeccable` | One-time design context setup | Writes `.impeccable.md` → Pencil reads it every session |
| `frontend-design` | Design principles + AI slop detection | Pencil's [AA] audit uses these principles on canvas |
| `critique` | Full UX critique with heuristics scoring | Run after [GC] code generation for code-level quality review |
| `audit` | Technical quality audit on code | Run after [GC] for performance, accessibility, and standards checks |

**Impeccable workflow with Pencil:**
1. `teach-impeccable` → establishes `.impeccable.md` (one-time)
2. Pencil reads `.impeccable.md` + `DESIGN.md` every session (automatic)
3. Pencil designs screens with these principles internalized
4. [GC] generates code → `critique` reviews the code → feedback to Pencil if needed
5. Final `polish` pass on the code before shipping

**MCP Tools** (if available):
| Tool | What Pencil Uses It For |
|---|---|
| `XcodeBuildMCP` | Boot simulator for [RE] capture, build after [GC] code gen |
| `Chrome DevTools MCP` | [RE] web capture, CSS extraction, responsive screenshots |
| `Refero MCP` | Design research and pattern reference |

### User-Provided Tools

_Additional MCP servers or services the owner has made available. Document them here._
