---
name: theme-variants
description: Generate light/dark mode variants or alternative color schemes side by side
code: TV
---

# Theme Variants

Generate theme variants of existing screens — light/dark mode, or alternative color schemes — placed next to the originals for comparison.

## What Success Looks Like

Side-by-side screenshots: original theme (left), variant (right). Contrast ratios verified and passing. Owner can immediately see how the app looks in both modes before any code changes.

## Theme Token Mapping

Read DESIGN.md for both light and dark palette values. Build the mapping:

| Token | Light | Dark |
|---|---|---|
| `$bg` | #FFFFFF | #09090B |
| `$surface` | #F4F4F5 | #18181B |
| `$text-primary` | #000000 | #FAFAFA |
| `$text-secondary` | #71717A | #A1A1AA |
| `$border` | #E4E4E7 | #27272A |

Note: some tokens invert non-obviously (text-secondary ↔ text-tertiary). Read DESIGN.md values — don't assume simple inversion.

## Process

1. Read source frame: `batch_get({nodeIds: [id], readDepth: 10, resolveVariables: true})`
2. Detect current theme from background color
3. Find position: `find_empty_space_on_canvas({direction:"right"})` 
4. Copy the source screen: `C(source-id, "document", {})`
5. Swap all color values using the mapping table
6. Run contrast verification with `scripts/contrast-ratio.py`
7. Screenshot both, present side by side

## Contrast Verification

Run for every critical text/background pair:

```bash
python3 scripts/contrast-ratio.py --fg "#FAFAFA" --bg "#09090B"
```

Minimum requirements:
- Body text on background: 4.5:1 (AA)
- Large text on background: 3:1 (AA)
- Text on surface cards: 4.5:1 (AA)

Flag failures with suggested fixes.

## Alternative Color Schemes

For explorations beyond light/dark: apply the new palette to a copy of the screen. Strategies:
- Temperature shift: warm/cool tint on neutrals
- Accent swap: change primary accent only
- High contrast: increase all contrast ratios by 1 tier

## Batch Variants

**Confirm scope first:** Ask: "Generate [light/dark/scheme name] variants for all N screens, or specific screens?" Generating variants creates N new frames — confirm before proceeding.

For 5+ screens: spawn subagents to read structures in parallel. Each returns compact JSON (max 250 tokens):

```json
{
  "screen": "Dashboard",
  "frame_id": "dashboard-001",
  "current_theme": "light",
  "color_nodes": 14,
  "token_bound": 11,
  "hardcoded": 3,
  "hardcoded_values": ["#F5F5F5", "#E5E5E5", "#333333"]
}
```

Use the inventory to determine which screens need manual node-by-node swaps vs. which will auto-switch via themed variables, then generate variants sequentially.

## After the Session

Follow the standard session close protocol. Additionally log: which theme approach the owner preferred, any new theme tokens needed for DESIGN.md update.
