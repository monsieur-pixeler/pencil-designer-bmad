# Pulse

**Default frequency:** Weekly, or after significant design sessions

## On Quiet Rebirth

When invoked via `--headless` without a specific task, load `references/memory-guidance.md` for memory discipline, then work through these in priority order.

### Memory Curation

Your goal: when your owner activates you next session and you read MEMORY.md, you should have everything you need to be effective and nothing you don't.

Review session logs in `sessions/`. Distill into MEMORY.md:
- Design decisions made and their rationale (the ones that might be revisited)
- Approval patterns observed (add to BOND.md taste tracking)
- Components created — update `component-registry.md`
- WDS batch generation progress if in-flight
- Token mappings established (DESIGN.md → Pencil variable names)

Prune session logs older than 14 days once their value is captured.

### Design System Health

Check the project's design system for drift. For each active project in MEMORY.md:

1. **Token drift** — compare Pencil variables with code tokens (Swift DesignSystem/, CSS vars, Tailwind config). Flag any mismatch.
2. **Hardcoded values** — scan source files for color/font/spacing values that should be tokens. Use `scripts/scan-hardcoded-values.py` if available.
3. **Component reuse rate** — check `component-registry.md` against current .pen file `batch_get({reusable: true})`. Flag orphaned components and underused patterns.
4. **DESIGN.md sync** — verify all DESIGN.md tokens are present as Pencil variables.

Write the health report to the session log. If score < 70 (rough estimate), flag `health_alert: true` in MEMORY.md so next session opens with a note.

### Self-Improvement

Reflect on recent sessions. What design patterns did the owner keep approving? What got pushed back? Are there capabilities the owner keeps needing that aren't built in? Note improvement opportunities in session log for discussion next session.

## Task Routing

| Task | Action |
|------|--------|
| `health` or `drift` | Run Design System Health check only |
| `curate` | Run memory curation only |
| `audit` | Run both health + memory |
| `design {screen}` | Design the specified screen headlessly, screenshot, log result |
| `export` | Export all screens as PNG to `_bmad-output/designs/` |

## Quiet Hours

None by default — design work is async-friendly.

## State

_Maintained by the agent. Last check timestamps, pending items._

- Last health check: {not yet run}
- Last curation: {not yet run}
