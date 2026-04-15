---
name: framer-motion
description: Specify animations and transitions for Pencil designs, generate Framer Motion React code
code: FM
---

# Framer Motion

Add animation specifications to Pencil designs and generate Framer Motion code. Covers entrance animations, scroll animations, hover/tap interactions, page transitions, gesture animations, and orchestrated sequences.

## What Success Looks Like

Each screen has a clear animation specification: what animates, when, how. The generated Framer Motion code matches the visual design in Pencil. The owner can drop the code into their React project and see the design come to life immediately.

## Workflow

1. **Read the design** — `batch_get` on the target screen to understand the element hierarchy
2. **Define animation intent** — which elements animate, in what order, with what feel
3. **Generate Framer Motion code** — `motion` components wrapping the relevant elements
4. **Annotate the Pencil frame** — add annotation nodes to mark animated elements and their properties

## Animation Categories

### Entrance Animations (Page Load / Mount)

Elements appearing for the first time. Use `initial` + `animate`:

```tsx
// Fade up — standard entrance for content sections
<motion.div
  initial={{ opacity: 0, y: 24 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
>

// Stagger children — for lists, grids, feature cards
<motion.div
  variants={{
    hidden: {},
    show: { transition: { staggerChildren: 0.08 } }
  }}
  initial="hidden"
  animate="show"
>
  <motion.div
    variants={{
      hidden: { opacity: 0, y: 16 },
      show: { opacity: 1, y: 0, transition: { duration: 0.35, ease: "easeOut" } }
    }}
  />
```

### Scroll Animations

Elements that animate as they enter the viewport. Use `whileInView`:

```tsx
<motion.div
  initial={{ opacity: 0, y: 40 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, margin: "-100px" }}
  transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}
>
```

### Hover / Tap Interactions

Interactive feedback. Use `whileHover` + `whileTap`:

```tsx
// Button with press feel
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.97 }}
  transition={{ type: "spring", stiffness: 400, damping: 25 }}
>

// Card lift on hover
<motion.div
  whileHover={{ y: -4, boxShadow: "0 12px 40px rgba(0,0,0,0.12)" }}
  transition={{ duration: 0.2, ease: "easeOut" }}
>
```

### Page Transitions

Route changes with AnimatePresence:

```tsx
import { AnimatePresence, motion } from "framer-motion"

const pageVariants = {
  initial: { opacity: 0, x: 20 },
  enter: { opacity: 1, x: 0, transition: { duration: 0.3, ease: [0.16, 1, 0.3, 1] } },
  exit: { opacity: 0, x: -20, transition: { duration: 0.2, ease: "easeIn" } }
}

<AnimatePresence mode="wait">
  <motion.div
    key={router.pathname}
    variants={pageVariants}
    initial="initial"
    animate="enter"
    exit="exit"
  />
</AnimatePresence>
```

### Gesture Animations (Drag, Swipe)

```tsx
// Swipeable card
<motion.div
  drag="x"
  dragConstraints={{ left: -100, right: 100 }}
  dragElastic={0.1}
  onDragEnd={(_, info) => {
    if (Math.abs(info.offset.x) > 80) handleSwipe(info.offset.x > 0 ? "right" : "left")
  }}
>

// Pull-to-refresh pattern
<motion.div
  drag="y"
  dragConstraints={{ top: 0, bottom: 0 }}
  dragElastic={{ top: 0.3, bottom: 0 }}
>
```

### Number Counters / Progress

```tsx
// Animated counter
import { useMotionValue, useSpring, useTransform } from "framer-motion"

const count = useSpring(0, { stiffness: 100, damping: 30 })
useEffect(() => { count.set(targetValue) }, [])
const display = useTransform(count, (v) => Math.round(v))

<motion.span>{display}</motion.span>

// Progress bar
<motion.div
  initial={{ scaleX: 0 }}
  animate={{ scaleX: percentage / 100 }}
  style={{ originX: 0 }}
  transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
/>
```

### Layout Animations (Reorder / Expand)

```tsx
// Expanding card / accordion
<motion.div layout transition={{ layout: { duration: 0.3, ease: "easeInOut" } }}>
  <motion.div layout="position">
    {/* header always visible */}
  </motion.div>
  <AnimatePresence>
    {isOpen && (
      <motion.div
        initial={{ height: 0, opacity: 0 }}
        animate={{ height: "auto", opacity: 1 }}
        exit={{ height: 0, opacity: 0 }}
        transition={{ duration: 0.3 }}
      >
        {/* expandable content */}
      </motion.div>
    )}
  </AnimatePresence>
</motion.div>
```

## Annotating Pencil Designs

For each animated element, add an annotation frame next to it. Read the annotation color from BOND.md or the project's variables — look for `$annotation-animation` or `$annotation-fm`. If neither exists, create the variable in the .pen file (suggest a color that contrasts with other annotations in the project):

```javascript
// Annotation badge — uses project annotation variable, not hardcoded color
anno=I(parent,{type:"frame",cornerRadius:4,fill:"$annotation-animation",padding:[4,8],layout:"horizontal",gap:4})
I(anno,{type:"text",content:"FM",fontFamily:"$body",fontSize:10,fontWeight:"700",fill:"#FFFFFF"})
I(anno,{type:"text",content:"fade-up 0.4s",fontFamily:"$body",fontSize:10,fill:"#FFFFFF",opacity:0.7})
```

Use a distinct color for animation annotations to distinguish from design notes — define it as a variable, never hardcode.

## Animation Decision Framework

| Element Type | Recommended Animation |
|---|---|
| Page / screen entrance | Fade up (y: 20→0, opacity: 0→1) |
| Hero headline | Fade up, delay 0s |
| Hero subtext | Fade up, delay 0.1s |
| CTA button | Fade up, delay 0.2s + whileHover scale |
| Feature cards | Stagger fade up, 0.08s between |
| Navigation / header | Fade in (opacity only, no translate) |
| Modal / sheet | Scale from 0.95 + fade |
| List items | Stagger fade up |
| Progress bars | scaleX from 0, spring |
| Numbers/stats | useSpring counter |
| Image reveals | Clip reveal or fade |
| Page transitions | Fade + subtle slide |
| Buttons | whileTap scale 0.97, spring |

## Spring Presets

```tsx
// Snappy — buttons, interactive elements
{ type: "spring", stiffness: 400, damping: 25 }

// Smooth — page transitions, content
{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }

// Gentle — decorative, background elements
{ duration: 0.6, ease: "easeOut" }

// Bouncy — success states, gamification
{ type: "spring", stiffness: 200, damping: 12 }
```

## Full Screen Animation Spec

When annotating a complete screen, generate a spec document alongside the code:

```
Screen: Dashboard
Animations:
  Header      — fade in (opacity), duration 0.3s, delay 0
  Metric card — fade up (y:20), duration 0.4s, delay 0.1s
  Feature grid — stagger fade up, 0.08s between, starting delay 0.2s
  CTA button  — fade up, delay 0.4s + whileHover scale(1.02) whileTap scale(0.97)

Scroll triggers (if web):
  Features section — whileInView fade up, once:true
  Testimonial — whileInView fade up, margin: -100px
```

## Memory Integration

Note the owner's animation preferences in BOND.md (prefers subtle vs. dramatic, bounce vs. smooth). Log which animation patterns were approved. After 3+ sessions, synthesize into a project animation system note in MEMORY.md.

## After the Session

Log: which screens received animation specs, which Framer Motion patterns were used, any animation preferences revealed.
