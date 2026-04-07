---
name: animate
description: Specify animations and transitions for Pencil designs — auto-detects framework (SwiftUI or Framer Motion) from BOND.md
code: AN
aliases: [FM, SA]
---

# Animate

Add animation specifications to Pencil designs and generate framework-specific code. Auto-detects the target framework from BOND.md. Works for both SwiftUI and React (Framer Motion).

## Framework Detection

1. Read BOND.md → check "Their Code Framework" section
2. If **SwiftUI** → load `references/animate-swiftui.md` and follow it
3. If **React / Tailwind / Next.js** → load `references/animate-framer-motion.md` and follow it
4. If **both** (multi-platform project) → ask: "This project uses both SwiftUI and React. Which platform are we animating for right now?"
5. If **unknown** (BOND.md not yet filled, or framework not set) → ask: "What's your code framework — SwiftUI or React?"

Never guess. Always confirm before generating code.

## What Success Looks Like

Each screen has a clear animation specification: what animates, when, how. The generated code matches the visual design in Pencil. The owner can drop the code into their project and see the design come to life immediately.

## Shared Workflow (Both Frameworks)

1. **Read the design** — `batch_get` on the target screen to understand the element hierarchy
2. **Define animation intent** — which elements animate, in what order, with what feel
3. **Generate framework-specific code** — dispatch to the appropriate sub-reference
4. **Annotate the Pencil frame** — add annotation nodes to mark animated elements

## Platform-Agnostic Animation Intent

Before generating code, define the intent in platform-neutral terms. These annotations live on the Pencil frame and survive framework switches:

| Element Type | Intent | Feel |
|---|---|---|
| Screen entrance | fade-up, 0.4s | spring/standard |
| Hero headline | fade-up, delay 0s | standard |
| Supporting content | fade-up, delay 0.1–0.2s | standard |
| CTA button | fade-up + press-scale | snappy |
| List/grid items | stagger fade-up, 0.08s between | standard |
| Navigation push | slide-right | smooth |
| Sheet/modal | slide-up + fade, scale 0.95→1 | smooth |
| Shared element (gallery→detail) | matched-geometry | smooth |
| Multi-step sequence | phase-sequence | custom |
| Counter/stat | number-roll | spring |
| Progress bar | width-expand | spring |
| Toggle/switch | spring-toggle, 0.2s | snappy |

## Annotating Pencil Designs

For each animated element, add an annotation badge. Read the annotation color from variables — look for `$annotation-animation`. If it doesn't exist, create it:

```javascript
anno=I(parent,{type:"frame",cornerRadius:4,fill:"$annotation-animation",padding:[4,8],layout:"horizontal",gap:4})
I(anno,{type:"text",content:"AN",fontFamily:"$body",fontSize:10,fontWeight:"700",fill:"#FFFFFF"})
I(anno,{type:"text",content:"fade-up 0.4s spring",fontFamily:"$body",fontSize:10,fill:"#FFFFFF",opacity:0.7})
```

## Full Screen Animation Spec

When annotating a complete screen, generate a platform-agnostic spec first:

```
Screen: Dashboard
Framework: {detected from BOND.md}

Animations:
  Header        — fade-up, 0.3s standard, delay 0
  Metric cards  — stagger fade-up, 0.08s between, delay 0.1s
  CTA button    — fade-up 0.4s + press-scale snappy
  Tab indicator — spring-toggle on selection change

Transitions:
  Push to detail — slide-right smooth
  Metric → chart — matched-geometry
```

Then generate the framework-specific code by loading the appropriate sub-reference.

## Spring Presets (Cross-Framework)

| Name | Feel | When to use |
|---|---|---|
| Snappy | Fast response, slight overshoot | Buttons, toggles, interactive elements |
| Standard | Balanced, no overshoot | Content entrances, list items |
| Smooth | Slow, no overshoot | Page-level transitions, sheets |
| Bouncy | Pronounced overshoot | Success states, celebrations |
| Gentle | Very slow, ease-out | Decorative, background elements |

Framework-specific values are in the sub-references.

## Memory Integration

Note the owner's animation preferences in BOND.md (prefers subtle vs. expressive, spring vs. easeOut, whether they use PhaseAnimator/AnimatePresence patterns). Log which animation patterns were approved. After 3+ sessions, synthesize into a project animation system note in MEMORY.md.

## After the Session

Log: which screens received animation specs, which framework was used, any animation preferences revealed.
