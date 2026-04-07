---
name: design-system-health
description: Automated health check comparing design tokens with code tokens, measuring component reuse, detecting drift
code: SH
---

# Design System Health

Automated audit comparing the .pen design system with the codebase. Detects drift before it becomes technical debt. Also runs automatically during Quiet Rebirth (Pulse).

## What Success Looks Like

A health score with specific, actionable drift findings. The owner knows exactly where design system and code have diverged and can fix it before it compounds.

## Checks

### 1. Token Drift

Compare `get_variables` with code token files:
- SwiftUI: `**/DesignSystem/ColorTokens.swift`, `**/Typography.swift`
- React: `**/globals.css`, `tailwind.config.*`
- CSS: `**/variables.css`

Flag mismatches:
```
✗ color.surface: Pencil #F4F4F5 ≠ Code #F5F5F5
⚠ spacing.section: 32px in Pencil, no code equivalent found
```

### 2. Hardcoded Values

Scan source files for values that match tokens but are hardcoded. Use `scripts/scan-hardcoded-values.py` if available.

### 3. Component Reuse Rate

```
Components defined: 12
Instances used: 47
Reuse rate: 3.9x (healthy: >2x)
Orphaned: 1 (ProfileCard — unused)
```

Cross-reference against `component-registry.md` in MEMORY.md.

### 4. DESIGN.md Sync

Are all DESIGN.md tokens present as .pen variables? Are there .pen variables missing from DESIGN.md?

## Health Score

```
Design System Health: 78/100

  Token sync:       80%  (2 drifted, 1 missing in code)
  Component reuse:  90%  (1 orphan)
  Hardcoded values: 60%  (8 found in code)
  DESIGN.md sync:   80%  (2 Pencil vars not documented)
```

## Headless Mode (Pulse)

When running automatically, run MCP-dependent and independent checks in parallel — don't wait for MCP before starting code-side checks:

**Parallel — start both immediately:**
- **MCP branch:** `get_editor_state` probe → if live, run token drift (Pencil side) and DESIGN.md sync; if unavailable, note `mcp_unavailable: true` and skip.
- **Code branch:** scan source files for hardcoded values (`scripts/scan-hardcoded-values.py`), compare code token files for drift, calculate component reuse rate from registry.

**After both branches complete:**
1. Merge results into a unified health score
2. Write report to session log
3. If score < 70, write `[ALERT] health_alert: true` to MEMORY.md — this gets immediate attention at next rebirth
4. If score recovers above 80, remove the alert entry

## Memory Integration

After every health check (interactive or Pulse), append to session log:
- Health score and date
- Top 1–3 specific findings (file:line or token name)
- Whether any fixes were applied

In MEMORY.md, maintain a single `Design System Health` entry. Overwrite it each Pulse run:
```
Design System Health: {score}/100 — last checked {date}
Top findings: {brief list or "clean"}
```

If score < 70: write `[ALERT] Design System Health below threshold ({score}/100) — review before next design session.` to MEMORY.md. This gets immediate attention at rebirth.
If score recovers above 80: remove the `[ALERT]` entry.

## Interactive Mode

Present full report with actionable fixes. Offer to:
- Fix token drift (update Pencil variables or code tokens)
- Remove orphaned components
- Tokenize hardcoded values

## After the Session

Log health score and top findings. If accepting fixes, log what was changed.
