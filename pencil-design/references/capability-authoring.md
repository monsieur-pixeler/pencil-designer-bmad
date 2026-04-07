---
name: capability-authoring
description: Guide for creating and evolving learned design capabilities
---

# Capability Authoring

When the owner wants Pencil to learn a new design ability — a specific component pattern, a new workflow, a domain-specific technique — we create a capability together.

## When to Create a Learned Capability

- A component pattern the owner uses repeatedly but isn't in the built-in patterns
- A design workflow specific to their tech stack or WDS setup
- A project-specific convention (e.g., "our card system always has these 3 variants")
- A design technique they want me to master (e.g., "always apply our ADHD-optimized layout rules")

## Capability Format

Every learned capability is a markdown file in `capabilities/` with this frontmatter:

```markdown
---
name: {kebab-case-name}
description: {one line — what this does}
code: {2-letter code, unique across all capabilities}
added: {YYYY-MM-DD}
type: prompt | script | multi-file
---
```

The body should be **outcome-focused**:

- **What Success Looks Like** — the design output, not the steps
- **Context** — constraints, tokens to use, platform considerations
- **Pattern** — the batch_design operations or approach (include concrete examples)
- **Memory Integration** — how to use MEMORY.md / BOND.md to personalize
- **After Use** — what to capture in the session log

## Creating a Capability (The Flow)

1. Owner describes what they want Pencil to do
2. Explore through conversation — understand the pattern, the context, the output
3. Draft the capability prompt and show it
4. Refine based on feedback
5. Save to `capabilities/{name}.md`
6. Update CAPABILITIES.md — add a row to the Learned table
7. Update INDEX.md — note the new file
8. Confirm: "I'll know how to do this next session. Trigger it with [{code}] or just ask."

## Design-Specific Capability Types

### Component Pattern
A batch_design operations template for a specific UI element. Include:
- The full I() operations with token placeholders
- When to use it vs. built-in patterns
- Variants (active/inactive, with/without icon, etc.)

### Workflow
A design process for a specific context (e.g., "design WDS screens for a fitness app"). Include:
- WDS artifact locations specific to their project
- Which DESIGN.md sections to prioritize
- Approval patterns to apply from BOND.md

### Convention
A project rule (e.g., "navigation always uses these specific icons"). Include:
- The rule with concrete examples
- When it applies and exceptions
- How to verify compliance in screenshots

## Refining Capabilities

After use, if the owner gives feedback:
- Update the capability prompt
- Note what worked and what didn't in session log
- A capability refined 3-4 times is usually excellent

## Retiring Capabilities

If a capability is superseded:
- Remove from CAPABILITIES.md Learned table
- Keep the file (don't delete — might be useful later)
- Note the retirement in session log
