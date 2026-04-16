---
name: design-to-code
description: Generate production code from Pencil designs, or recreate existing code as Pencil designs
code: GC
---

# Generate Code & Code to Design

Bidirectional: translate Pencil designs into production code, or recreate existing code as visual designs for iteration.

## Design → Code

### What Success Looks Like
Production-ready code in the owner's framework that matches the Pencil design. Uses design tokens as code tokens (not hardcoded values). Extracts reusable components as separate View/Component definitions.

### Reading the Design
`batch_get({nodeIds: [frame-id], readDepth: 10, resolveVariables: true})` — read with resolved values. `get_variables` — get token definitions for proper mapping.

### Node → UI Element Translation

| Pencil Node | SwiftUI | React/Tailwind |
|---|---|---|
| `frame` layout:vertical | `VStack(spacing:)` | `flex flex-col gap-` |
| `frame` layout:horizontal | `HStack(spacing:)` | `flex flex-row gap-` |
| `frame` layout:none | `ZStack` | `relative` |
| `text` | `Text().font().fontWeight()` | `<span className="text- font-">` |
| `rectangle` | `Rectangle().fill()` | `<div className="bg-">` |
| `icon_font` (lucide) | `Image(systemName:)` equiv | `<Icon />` from lucide-react |
| `ref` (instance) | Extracted SwiftUI View | Extracted React component |

### Layout Properties

| Pencil | SwiftUI | Tailwind |
|---|---|---|
| `gap: 32` | `spacing: 32` | `gap-8` |
| `padding: [0,24]` | `.padding(.horizontal, 24)` | `px-6` |
| `width: "fill_container"` | `.frame(maxWidth: .infinity)` | `w-full` |
| `cornerRadius: 16` | `.clipShape(RoundedRectangle(cornerRadius: 16))` | `rounded-[16px]` |
| `fill: color` | `.background(Color)` | `bg-[color]` |

### Framework-Specific Notes

**SwiftUI:** Lucide icons → SF Symbols equivalents. Grouped lists → `List(.insetGrouped)`. Tab bars → `TabView`.

**React + Tailwind:** Lucide icons → `lucide-react`. Use shadcn/ui primitives if owner uses them. Map Pencil variables → Tailwind config tokens.

### Workflow
1. Ask target framework (or read from BOND.md if known)
2. Read frame with `batch_get` + `resolveVariables: true`
3. Generate code using design tokens, not hardcoded values
4. Extract reusable components as separate definitions
5. Show screenshot alongside generated code for comparison

## Code → Design

### What Success Looks Like
A Pencil frame that accurately represents the code component — ready for visual iteration without touching code.

### Process
1. Read source code — understand structure, layout, styling
2. Map code tokens back to Pencil variables (MEMORY.md has these if established)
3. `batch_design` — translate code structure to Pencil nodes
4. Screenshot and compare against running app (if available)

### Reverse Mapping

| SwiftUI | Pencil |
|---|---|
| `VStack(spacing: N)` | `{layout:"vertical", gap:N}` |
| `HStack(spacing: N)` | `{layout:"horizontal", gap:N}` |
| `.background(Color.X)` | `fill: "hex-value"` |
| `.padding(N)` | `padding: N` |
| `Image(systemName: "name")` | `{type:"icon_font", iconFontFamily:"lucide", ...}` |

## Token Sync

Keep Pencil variables and code tokens in sync. After design changes, export variables with `get_variables` and update Swift DesignSystem/ or CSS vars. After code token changes, re-read and update .pen variables.

## Design-Reality Verification (after code generation)

After generating code, offer to verify the output matches the design:

**For web/Tauri projects (Impeccable available):**

Check if Impeccable is installed (look for `.claude/skills/impeccable/`). If available:

```
"Code generated. Want me to run Impeccable's quality check?
This will scan the generated code for design anti-patterns."
```

If approved:
1. Run `npx impeccable --json {generated-file}` for deterministic anti-pattern detection
2. If the app is running in a browser: suggest `npx impeccable live` for visual overlay inspection, or the Chrome Extension for one-click checking
3. Report findings and offer to fix issues in the design or code

**For SwiftUI projects (XcodeBuildMCP available):**

Check if XcodeBuildMCP tools are available. If so:

```
"Code generated. Want me to build and screenshot in the simulator
to compare with the Pencil design?"
```

If approved:
1. Build the project via XcodeBuildMCP
2. Take simulator screenshot
3. Compare side-by-side with the Pencil `get_screenshot` of the original design
4. Flag visual differences: spacing, colors, typography, alignment

**When neither is available:** Skip verification. The generated code stands on its own.

## Memory Integration

Store established token mappings in MEMORY.md. Note owner's framework preference in BOND.md.

## After the Session

Log: which screens/components were translated, any mapping decisions, framework preferences confirmed. If verification ran, log findings and whether design or code was adjusted.
