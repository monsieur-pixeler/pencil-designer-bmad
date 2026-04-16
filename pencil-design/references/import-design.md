---
name: import-design
description: Analyze existing Pencil designs to extract patterns, tokens, and component opportunities
code: ID
---

# Import Design

Analyze an existing .pen file or selected frames to extract design patterns, identify potential design tokens, and find component extraction opportunities.

## What Success Looks Like

An actionable design system audit: what's consistent, what varies, what should be tokenized, what should be componentized. The owner walks away knowing what their current design system looks like in practice.

## Process

1. `batch_get` with full depth on selected frames (or all top-level frames)
2. `search_all_unique_properties` to find all unique color, font, and spacing values
3. `get_screenshot` of each frame for visual context
4. Analyze: identify patterns, inconsistencies, tokenization opportunities

## Analysis Areas

**Color audit:** All unique fill/stroke values. Which are consistent across frames? Which are one-offs? Map to potential token names.

**Typography audit:** All unique fontFamily/fontSize/fontWeight combinations. What's the hierarchy? What's consistent?

**Spacing audit:** All unique gap/padding values. Is there a rhythm? What should be a token?

**Component opportunities:** Recurring structures (3+ instances of the same pattern). Which should be `reusable: true` components?

**Token drift:** Values that almost match (e.g., #F4F4F5 and #F5F5F5) — these indicate drift and should be unified.

## Output

Present findings as a design system audit:
```
Color System:
  8 consistent colors → suggest token names
  3 one-off colors → review for elimination

Typography Scale:
  5 consistent styles → suggest named styles
  2 inconsistencies → suggest resolution

Component Opportunities:
  "Section header" pattern: 7 instances → create component
  "Metric row" pattern: 5 instances → create component
```

Offer to: initialize design tokens from audit, create reusable components from patterns.

## After the Session

Follow the standard session close protocol. Additionally log: audit findings, which suggestions were accepted vs. deferred. Update MEMORY.md with discovered token values and component patterns.
