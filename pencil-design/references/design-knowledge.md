---
name: design-knowledge
description: Universal design principles and anti-patterns — Pencil's internal quality rules informed by Impeccable. Loaded during audits and as standing design guidance.
---

# Design Knowledge

Pencil's internal design quality rules. These are platform-agnostic principles that apply to every screen designed on canvas. Informed by Impeccable's 25 deterministic detectors and cross-skill design principles.

Load this reference during [AA] App Audit, [AC] Accessibility Check, and when evaluating any completed screen.

## AI Slop Detection — 11 Tells

These patterns signal generic, undesigned output. Flag them in every audit and avoid them in every design:

| # | Pattern | How to detect in .pen | Severity |
|---|---|---|---|
| 1 | **Side-tab accent border** | Frame with one-side border >1px in accent color | High |
| 2 | **Border accent on rounded element** | Thick border on cornerRadius >8 frame | High |
| 3 | **Gradient text** | Text with gradient fill instead of solid | High |
| 4 | **AI color palette** | Purple/violet + cyan combination anywhere | High |
| 5 | **Dark mode + glowing accents** | Dark bg + colored shadow on elements | Medium |
| 6 | **Icon tile above heading** | Small rounded-square frame with icon, above text — repeated pattern | Medium |
| 7 | **Identical card grids** | 3+ frames with identical child structure + dimensions | Medium |
| 8 | **Everything centered** | >80% of top-level content frames use `alignItems: "center"` | Medium |
| 9 | **Monotonous spacing** | <3 unique gap/padding values across 5+ screens | Medium |
| 10 | **Flat type hierarchy** | Adjacent font sizes differ by <2px | Medium |
| 11 | **Single font** | Only one fontFamily across entire design | Low |

**The test:** If someone saw this design and said "AI made this," would they believe it immediately? If yes — redesign.

## Quality Rules — 14 Checks

| # | Rule | Canvas check | Severity |
|---|---|---|---|
| 12 | **Low contrast text** | `scripts/contrast-ratio.py` — body 4.5:1, large 3:1 (WCAG AA) | High |
| 13 | **Tiny body text** | Text nodes with fontSize <12 in body context | High |
| 14 | **Tight line height** | Text with lineHeight <1.3× fontSize | Medium |
| 15 | **Cramped padding** | Frame padding <8px with text children | Medium |
| 16 | **Nested cards** | Frame with cornerRadius inside another frame with cornerRadius | Medium |
| 17 | **Gray text on color** | Text fill is neutral gray on a non-white/non-gray background | Medium |
| 18 | **Pure black background** | Frame fill is exactly #000000 (should be tinted) | Low |
| 19 | **Justified text** | textAlign: "justified" without hyphenation | Low |
| 20 | **Line length too long** | Text frame width >700px without max-width constraint | Low |
| 21 | **Wide letter spacing on body** | letterSpacing >0.05em on body text | Low |
| 22 | **Skipped heading level** | Display 28→Body 15 with no intermediate size | Low |
| 23 | **All-caps body text** | Long text content (>20 chars) in uppercase | Low |
| 24 | **Bounce/elastic easing** | Animation spec with bounce/elastic — use ease-out instead | Low |
| 25 | **Layout property animation** | Animation spec targeting width/height — use transform/opacity | Low |

## 15 Universal Design Principles

These recur across multiple Impeccable skills and are always applicable:

### Color
1. **60-30-10 rule** — 60% dominant neutral, 30% secondary, 10% accent. Never equal distribution.
2. **Tinted neutrals** — Never pure gray. Always tint toward brand hue, even subtly.
3. **Never gray on color** — On colored backgrounds, use a shade of the background color, not neutral gray.
4. **OKLCH over HSL** — Perceptually uniform. Colors with same lightness actually look equally light.

### Typography
5. **Type scale ratio** — Minimum 1.25× between steps. 5 sizes cover most needs (caption/body/heading/subheading/display).
6. **Max 65-75ch line length** — Readability constraint. Beyond this, eyes lose their place.
7. **Max 2-3 font families** — One display, one body. Third only if needed for code/mono.

### Spacing
8. **4pt spacing scale** — 4/8/12/16/24/32/48/64/96. Everything snaps to this grid.
9. **Tight grouping vs generous separation** — Related items: 8-12px. Sections: 48-96px. The contrast creates rhythm.
10. **Never cards in cards** — Flatten the hierarchy. Visual noise from nesting.

### Composition
11. **Squint test** — Blur your eyes. Is the hierarchy still visible? If everything looks the same weight, it fails.
12. **Progressive disclosure** — Start simple. Reveal complexity on demand. Don't dump everything upfront.
13. **44×44px touch targets** — Minimum for touch interfaces. No exceptions.

### Motion
14. **Ease-out-quart/quint/expo** — Never bounce or elastic. Real objects decelerate smoothly.
15. **Exit = 75% of entrance** — Exits should be faster. 300ms entrance → 225ms exit.

## Empty State Formula

Every empty state screen must include:
1. **What will appear here** — set expectations
2. **Why it's valuable** — motivation
3. **CTA to get started** — clear action
4. **Visual interest** — not just text
5. **Contextual help** — link to more info if needed

## Cognitive Load Check

Per screen, count:
- **Primary actions** (buttons, toggles, links): flag if >7
- **Distinct sections** without progressive disclosure: flag if >5
- **Unique colors** used: flag if >8 (palette bloat)
- **Choices at each decision point**: flag if >4 visible options

Working memory holds ~4 items. Design for this limit.

## Font Selection (from Impeccable)

Avoid these overused "reflex fonts" — they signal generic, undesigned output:
Inter, Roboto, Open Sans, Lato, Montserrat, Arial, DM Sans, Space Grotesk, Fraunces, Playfair Display, Poppins, Nunito, Raleway, Source Sans, Work Sans, Manrope, Plus Jakarta Sans, Geist, Sora, Lexend, Albert Sans, Urbanist, Figtree

**Font selection process:**
1. Define 3 brand personality words
2. Reject reflex fonts above
3. Browse font catalogs (Google Fonts, Fontshare, Font Squirrel)
4. Cross-check: does this font appear on 1000+ other sites? If yes, keep looking.

## When to Load This Reference

- **Always during [AA] App Audit** — check all 25 rules
- **During [AC] Accessibility** — rules 12-13-14 supplement WCAG checks
- **After any [DP] design session** — quick scan of the 11 AI Slop tells
- **During [QG] quality discussions** — full reference available
- **First Breath** — share the 15 principles with the owner as "how I think about design"
