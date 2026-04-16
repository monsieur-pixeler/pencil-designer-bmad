---
name: capabilities-guide
description: Verbose reference for capability selection, design phases, ecosystem agents, and WDS orchestration
---

# Capabilities Guide

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
| **Create** | Building screens | `[DP]` design, `[PW]` wireframe→visual, `[WS]` from WDS specs, `[MV]` marketing, `[SN]` script nodes |
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
| Need a chart, gauge, or data visualization | `[SN]` script-nodes |
| Check design quality against principles | `[AA]` audit (loads `references/design-knowledge.md` automatically) |
| Checking token drift | `[SH]` design-system-health |
| Exporting for developers | `[DH]` design-handoff |

**[ID] vs [AA] vs [SH] — when to use which:**
- `[ID]` — first analysis of an unfamiliar file; extracts what's there and names it
- `[AA]` — ongoing audit of known screens; flags deviations from established system
- `[SH]` — automated health check comparing Pencil against code; runs in Pulse

## WDS Orchestration (Soft Suggestion Only)

When the owner starts a new project without specs or wireframes, **suggest but never require** WDS:

1. Check if WDS skills exist: look for `wds-agent-freya-ux`, `wds-3-scenarios`, or `wds-agent-saga-analyst` in available skills
2. If they exist: "I see you have WDS available. Want to plan your screens with Freya first, or jump straight into designing?"
3. If they don't exist: skip the suggestion entirely — go straight to [MAP] or [DS]
4. **Never block on WDS.** The owner can always choose "just design"

## Legacy Capability Aliases

These old codes still work — they redirect to the merged capability:

| Legacy Code | Redirects To | Mode |
|---|---|---|
| [FM] | [AN] Animate | Framer Motion (React) |
| [SA] | [AN] Animate | SwiftUI |
| [RP] | [MP] Multi-Platform | Preview mode (quick size check) |

## Ecosystem Agents (Orchestration Partners)

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
