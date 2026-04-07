# Pencil Design Agent

**Autonomous visual designer for [Pencil.dev](https://pencil.dev) canvas.**

Pencil is a BMad Method agent that turns design intent into pixel-perfect visual references — so code serves the vision, not the other way around. It lives in the Pencil.dev canvas, thinks spatially, and always leads with a screenshot.

## What Pencil Does

Pencil designs screens, manages design systems, and bridges design specs to production code. It works inside Pencil.dev via MCP tools — reading, creating, and modifying design nodes directly on the canvas.

### Design Phases

Capabilities are organized into a guided design journey. Jump to wherever you need — phases are navigation, not a waterfall:

```
Discover → Foundation → Map → Create → Refine → Validate → Deliver
                                                              ↑
                                                    Maintain (always)
```

### 15 Capabilities across 7 Phases

| Phase | Code | Capability | What It Does |
|-------|------|-----------|-------------|
| **Discover** | `[RE]` | Reverse Engineer | Reverse-engineer any app or website — capture, analyze, rebuild or reskin |
| | `[ID]` | Import Design | Analyze existing .pen files for tokens, patterns, and component opportunities |
| **Foundation** | `[DS]` | Design System Setup | Set up, import, or consolidate tokens — palette, typography, spacing, DESIGN.md |
| **Map** | `[MAP]` | App Map | Map your entire app on one canvas — screen inventory, flow grid, gap analysis |
| **Create** | `[DP]` | Design & Polish | Design screens, components, iterate on existing designs |
| | `[PW]` | Wireframe to Visual | Transform wireframes into polished visual designs |
| | `[WS]` | WDS Integration | Batch-generate screens from WDS scenario specs |
| | `[MV]` | Marketing Visual | Design landing pages, App Store screenshots, pitch decks |
| **Refine** | `[TV]` | Theme Variants | Generate light/dark mode and alternative color schemes |
| | `[MP]` | Multi-Platform | Recompose for iPad/macOS/web + preview mode for quick size checks |
| | `[AN]` | Animate | Specify animations — auto-detects SwiftUI or Framer Motion from project config |
| **Validate** | `[AC]` | Accessibility Check | WCAG and iOS/HIG audit — contrast, touch targets, safe areas |
| | `[AA]` | App Audit | Scan screens for design inconsistencies and token drift |
| | `[DD]` | Design Diff | Compare two versions of a screen with structural diff |
| | `[CH]` | Component Harvest | Extract reusable components from recurring patterns |
| **Deliver** | `[GC]` | Design to Code | Generate SwiftUI/React/HTML from designs (or reverse) |
| | `[DH]` | Design Handoff | Export screens and generate component documentation |
| **Maintain** | `[SH]` | Design System Health | Automated token drift detection, runs in Pulse (headless) |

Plus **learned capabilities** — teach Pencil new skills during sessions and it remembers them.

### Smart Intake

Pencil detects what you need based on your intent:

| You say... | Pencil does... |
|---|---|
| "New app, starting fresh" | Checks for WDS specs → suggests Freya or starts [MAP] |
| "Reverse engineer this app" | [RE] with clone, reskin, or pattern library mode |
| "Switching from React to SwiftUI" | [RE] discover → [DS] rebuild tokens → [MAP] or Create |
| "My design is a mess" | [ID] analyze → [DS] cleanup → [MAP] reorganize → [AA] audit |
| "Design the settings screen" | Straight to [DP] — no routing overhead |
| `[AC]` or any capability code | Direct access, always works |

### Memory Architecture

Pencil is a **memory agent** — it builds understanding of your project across sessions:

- **First Breath:** Onboarding conversation that learns your design system, platform, code framework, and taste
- **Sanctum:** Persistent identity files (persona, values, bond, memory, capabilities) loaded every session
- **Session logs:** Raw notes captured after every session
- **Pulse:** Headless mode for automated design system health checks and memory curation

### Automation Scripts

| Script | Purpose |
|--------|---------|
| `contrast-ratio.py` | WCAG contrast ratio calculator |
| `scan-hardcoded-values.py` | Detect hardcoded design values in source code |
| `diff-tokens.py` | Compare Pencil variables with code token files |
| `diff-nodes.py` | Structural diff of two Pencil node trees |
| `classify-token-drift.py` | Classify unique property values against design tokens |
| `aggregate-patterns.py` | Aggregate component pattern counts from parallel analyses |

All scripts include unit tests in `scripts/tests/`.

## Requirements

- **[Pencil.dev](https://pencil.dev)** — Desktop App or VS Code Extension with a `.pen` file open
- **[Claude Code](https://claude.ai/claude-code)** — Claude Code CLI or IDE extension
- **[uv](https://docs.astral.sh/uv/)** — Python package runner (for scripts)
- **BMad Method** (optional) — For full module integration with `_bmad/` config system

## Installation

### Quick Install (one command)

From your project root:

```bash
curl -fsSL https://raw.githubusercontent.com/monsieur-pixeler/pencil-designer-bmad/main/install.sh | bash
```

This copies the skill into `.claude/skills/pencil-design/` and you're ready to go.

### Manual Install

```bash
git clone https://github.com/monsieur-pixeler/pencil-designer-bmad.git /tmp/pencil-designer-bmad
cp -r /tmp/pencil-designer-bmad/pencil-design /path/to/your-project/.claude/skills/pencil-design
```

### BMad Module Registration (optional)

If your project uses the BMad Method with `_bmad/` configuration, run after installing:

```
/pencil-design setup
```

This registers Pencil as a BMad module:
- Writes module config to `_bmad/config.yaml` and `config.user.yaml`
- Registers capabilities in `_bmad/module-help.csv`
- Creates output directories

Without BMad, Pencil works fine as a standalone Claude Code skill — just skip this step.

### After Installation

On your first design session, Pencil will:

1. Run `init-sanctum.py` to scaffold its memory (`_bmad/memory/pencil-design/`)
2. Start **First Breath** — a setup conversation where it learns about your project
3. Ask about your design system, platforms, code framework, workflow preferences, and taste

After First Breath, every future session starts with Pencil reading its sanctum files and becoming itself again.

## Usage

### Interactive

```
"Map my entire app"
"Design the dashboard screen"
"Reverse engineer strongapp.com and reskin it with my brand"
"Polish this wireframe into a visual design"
"Generate SwiftUI code from the Settings screen"
"Run an accessibility check on all screens"
"Create light and dark theme variants"
"How does this look on iPad?"
"Animate the dashboard — fade up with stagger"
"My design is spaghetti — help me clean up"
```

### Headless (Pulse)

```bash
# Default: design system health check + memory curation
claude --skill pencil-design --headless

# Specific tasks
claude --skill pencil-design --headless -- "health"
claude --skill pencil-design --headless -- "curate"
claude --skill pencil-design --headless -- "export"
```

## Project Structure

```
pencil-design/
  SKILL.md                         # Bootloader — identity, intake router, activation
  assets/
    PERSONA-template.md            # Communication style and personality seed
    CREED-template.md              # Core values, standing orders, boundaries
    BOND-template.md               # Owner relationship — filled during First Breath
    MEMORY-template.md             # Long-term memory — grows over time
    CAPABILITIES-template.md       # Phase-based capability routing table
    PULSE-template.md              # Headless mode task definitions
    INDEX-template.md              # File index — anti-orphan discipline
    module.yaml                    # BMad module metadata
    module-setup.md                # BMad registration workflow
  references/
    first-breath.md                # Onboarding conversation guide
    memory-guidance.md             # Memory discipline and [ALERT] conventions
    capability-authoring.md        # Framework for creating learned capabilities
    app-map.md                     # [MAP] App Map
    pencil-patterns.md             # [DP] Core design
    design-system-setup.md         # [DS] Foundation
    animate.md                     # [AN] Animate (router)
    animate-framer-motion.md       # [AN] Framer Motion sub-reference
    animate-swiftui.md             # [AN] SwiftUI sub-reference
    multi-platform.md              # [MP] Multi-Platform + preview mode
    reverse-engineer.md            # [RE] Reverse Engineer + reskin
    ... (12 more capability files)
  scripts/
    init-sanctum.py                # First Breath scaffolding
    contrast-ratio.py              # WCAG contrast calculator
    scan-hardcoded-values.py       # Source code token violation scanner
    diff-tokens.py                 # Design ↔ code token comparison
    diff-nodes.py                  # Node tree structural differ
    classify-token-drift.py        # Token classification engine
    aggregate-patterns.py          # Pattern count aggregator
    merge-config.py                # BMad config writer
    merge-help-csv.py              # BMad help system writer
    tests/                         # Unit tests (71 tests)
```

## Design Philosophy

Pencil follows five core values:

1. **Screenshot is truth** — A design only exists when it can be seen
2. **Project tokens first** — Never invent values; read DESIGN.md, use what's there
3. **Composition over decoration** — Hierarchy through layout, weight, and spacing
4. **Reuse builds systems** — Three instances of a pattern make a component
5. **Progressive construction** — Placeholder first, content second, screenshot last

## License

MIT

## Credits

Built with the [BMad Method](https://github.com/bmadcode/BMAD-METHOD) agent framework.
Designed for [Pencil.dev](https://pencil.dev) visual design canvas.

Created by Ramon van Schie ([@monsieur-pixeler](https://github.com/monsieur-pixeler))
