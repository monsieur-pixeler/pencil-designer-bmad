---
name: session-close
description: Standard session close protocol — loaded from CREED, not per-capability
---

# Session Close Protocol

Before ending any session:

1. Write session log to `sessions/YYYY-MM-DD.md` with:
   - What was designed/built
   - Decisions made and rationale
   - What was approved/rejected
   - Follow-up items for next session

2. Update sanctum files with anything learned:
   - BOND.md — taste patterns, platform preferences
   - MEMORY.md — design decisions, component registry updates
   - INDEX.md — if new files were created

3. If `.impeccable.md` exists and design tokens changed: update the Design System section.

4. Check MEMORY.md line count — if approaching 200 lines, flag for Pulse curation.
