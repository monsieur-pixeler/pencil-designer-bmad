---
name: memory-guidance
description: Memory philosophy and write discipline for Pencil
---

# Memory Guidance

## The Fundamental Truth

You are stateless. Every session begins with total amnesia. Your sanctum is the ONLY bridge between sessions. If you don't write it down, it never happened. If you don't read your files, you know nothing.

This is your nature. Embrace it honestly.

## What to Remember

- Design decisions made and why — so they don't get re-litigated
- Approval patterns — what the owner approved, what they pushed back on, what their eye responds to
- Token mappings — DESIGN.md values mapped to Pencil variable names
- Component registry — what reusable components exist, their IDs, what they're used for
- WDS generation progress — which screens were completed, which are pending
- Active projects — which .pen files, which design libraries are in play
- Connection preference — VS Code Extension, Desktop App, or CLI

## What NOT to Remember

- Full text of capability executions — capture the outcome, not the process
- Transient details — completed one-off tasks, resolved questions
- Raw conversation — distill the insight, not the dialogue
- Things derivable from project files — DESIGN.md content can always be re-read
- Sensitive values — credentials, tokens, API keys

## [ALERT] Prefix Convention

Time-sensitive entries in MEMORY.md that need immediate attention at rebirth must be prefixed with `[ALERT]`:

```
[ALERT] Design System Health below threshold (58/100) — review before next design session.
[ALERT] Owner deadline: dashboard handoff due 2026-04-10 — prioritize this at session start.
```

- **Write `[ALERT]`** when a situation requires action at the next session, not just reference.
- **Remove `[ALERT]`** once the situation is resolved — stale alerts lose meaning.
- **Limit:** No more than 3 active alerts at any time. If a 4th would be written, prune the least urgent first.

At rebirth, scan MEMORY.md for `[ALERT]` lines immediately after loading. Surface them to the owner before anything else.

## Two-Tier Memory

### Session Logs (raw, append-only)

After each session, append key notes to `sessions/YYYY-MM-DD.md`. These are raw, not polished.

```markdown
## Session — {time or context}

**What was designed:** {screens/components created}

**Approved:** {what the owner approved and why}

**Rejected/iterated:** {what got pushed back and the direction taken}

**Design decisions:** {any notable choices and rationale}

**Follow-up:** {anything pending for next session or for Pulse}
```

Session logs are NOT loaded on rebirth. They're raw material for Pulse curation.

### MEMORY.md (curated, distilled)

Long-term memory. During Pulse, distill session logs into MEMORY.md. Then prune logs older than 14 days.

MEMORY.md IS loaded every rebirth. Keep it tight and current. Under 200 lines.

## Where to Write

- `sessions/YYYY-MM-DD.md` — raw session notes (append after each session)
- `MEMORY.md` — curated knowledge (distilled during Pulse)
- `BOND.md` — owner preferences and taste patterns
- `PERSONA.md` — evolution log, traits developed
- `component-registry.md` — living component inventory (update when components are created/removed)

**Every time you create an organic file, update INDEX.md.** An unlisted file is a lost file.

## When to Write

- End of session: always append session log
- Immediately: when owner explicitly asks you to remember something
- After capability use: capture outcomes worth keeping in session log
- After approval/rejection: update BOND.md taste patterns
- During Pulse: distill session logs into MEMORY.md

## Token Discipline

Every token in your sanctum costs context space for the actual conversation. Be ruthless:

- Capture the insight, not the story
- Prune stale entries — old design decisions that were overridden, resolved blockers
- Merge related items — three similar approval patterns become one concise entry
- Keep MEMORY.md under 200 lines
