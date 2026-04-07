---
name: design-system-setup
description: Interactively set up or import a design system — tokens, palette, typography, spacing grid, DESIGN.md bootstrap
code: DS
---

# Design System Setup

Establish the design foundation before designing a single screen. Creates or imports design tokens (colors, typography, spacing), writes them to Pencil variables, and bootstraps DESIGN.md.

Three modes depending on where you're coming from:

| Mode | When | Input |
|---|---|---|
| **Interactive** | New project, no design system yet | Owner's preferences (conversation) |
| **Import** | After Discover ([RE] or [ID]) | Extracted tokens from analysis |
| **Cleanup** | Spaghetti project, inconsistent tokens | Existing .pen variables → consolidate |

## What Success Looks Like

A complete set of Pencil variables (`set_variables`) covering colors, typography, and spacing. A DESIGN.md file that documents the system. Every future design decision references tokens, never hardcoded values.

## Interactive Mode — Building from Scratch

### Step 1: Gather Design Intent

Ask conversationally — don't make it a form:

"What's the vibe of your app? Pick what resonates:
- **Light and clean** (white backgrounds, subtle grays)
- **Dark and focused** (dark backgrounds, high contrast)
- **Warm and organic** (cream, warm grays, soft edges)
- **Bold and vibrant** (saturated colors, strong accent)
- Or describe your own..."

### Step 2: Color Palette

Based on the vibe, propose a palette:

```
Proposed Palette: Light and Clean

Background:      #FFFFFF → $bg
Surface:         #F4F4F5 → $surface
Border:          #E4E4E7 → $border
Text Primary:    #18181B → $text-primary
Text Secondary:  #71717A → $text-secondary
Text Tertiary:   #A1A1AA → $text-tertiary
Accent:          #F97316 → $accent (orange — adjust if needed)
Success:         #22C55E → $success
Error:           #EF4444 → $error
```

"Does this feel right? Want to adjust any colors? What's your brand accent color?"

### Step 3: Typography

```
Proposed Typography:

Display:  Outfit — headings, hero text, numbers
Body:     Inter — body text, labels, descriptions

Type Scale:
  Display Large:  28px / 800 weight → $display-large
  Display:        24px / 700 weight → $display
  Heading:        20px / 600 weight → $heading
  Body:           15px / 400 weight → $body
  Caption:        13px / 500 weight → $caption
  Small:          11px / 500 weight → $small
```

"Using Outfit + Inter unless you have a different preference?"

### Step 4: Spacing Grid

```
Proposed Spacing: 8px grid

  4px   — tight (icon padding, badge insets)
  8px   — compact (inside small elements)
  12px  — snug (list item gaps)
  16px  — standard (card padding, form gaps)
  24px  — comfortable (section padding)
  32px  — spacious (section gaps)
  48px  — wide (major section separation)
  64px  — extra (page-level separation)

Corner Radius:
  Small:  8px  → buttons, badges, inputs
  Medium: 16px → cards, sheets
  Large:  24px → modal overlays, hero cards
```

### Step 5: Write Everything

1. `set_variables` — write all tokens to the .pen file
2. Generate `DESIGN.md` at `{project-root}/DESIGN.md`:

```markdown
# Design System

## Colors
| Token | Hex | Usage |
|---|---|---|
| $bg | #FFFFFF | Page background |
| $surface | #F4F4F5 | Cards, grouped sections |
...

## Typography
| Token | Font | Size | Weight | Usage |
|---|---|---|---|---|
| $display-large | Outfit | 28px | 800 | Hero headings |
...

## Spacing
8px grid: 4, 8, 12, 16, 24, 32, 48, 64

## Corner Radius
Small: 8px, Medium: 16px, Large: 24px
```

3. Screenshot the variable panel for confirmation

## Import Mode — From Discover Results

When coming from [RE] Reverse Engineer or [ID] Import Design, the tokens are already extracted.

1. Read the analysis results (extracted colors, typography, spacing)
2. Present: "I found these tokens in the analysis. Import as-is, or adjust?"
3. For reskin: show dual token system (source → target mapping)
4. Write to Pencil variables + DESIGN.md

## Cleanup Mode — Consolidating Spaghetti

When the Discover diagnose-modus flagged inconsistent tokens:

1. Read current `get_variables` from the .pen file
2. Read `search_all_unique_properties({properties: ["fill", "fontFamily", "fontSize", "gap", "padding"]})` for all hardcoded values
3. Present a consolidation plan:

```
Token Consolidation:

Colors found: 14 unique → consolidating to 6 tokens
  #F4F4F5, #F5F5F5, #F3F3F4 → all become $surface (#F4F4F5)
  #71717A, #737373, #6B7280 → all become $text-secondary (#71717A)
  ...

Typography found: 8 unique combinations → consolidating to 5 styles
  Outfit 28/800 and Outfit 26/700 → both become $display (28/800)
  ...

Approve this consolidation? I'll update all frames automatically.
```

4. On approval: `replace_all_matching_properties` for each consolidation
5. `set_variables` with the cleaned token set
6. Generate or update DESIGN.md

## When DS Runs Implicitly

Foundation [DS] doesn't always need to be explicitly invoked:

- **First Breath** already collects design system info → DS writes the tokens
- **[WS] WDS Integration** checks for tokens at the start → runs DS if missing
- **[DP] Design & Polish** reads DESIGN.md → suggests DS if no tokens exist
- **[RE] Reverse Engineer** extracts tokens → hands off to DS for import

DS is the **writing mechanism** — other capabilities trigger it when tokens are missing.

## Memory Integration

Store the design system summary in MEMORY.md:
```
Design System: established {date}
Palette: light mode, 6 colors, accent #F97316
Typography: Outfit (display) + Inter (body)
Spacing: 8px grid
```

## After the Session

Log: which tokens were established/imported/consolidated, DESIGN.md location, any design decisions made.
