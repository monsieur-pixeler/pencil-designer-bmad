---
name: marketing-visual
description: Design landing pages and marketing visuals — orchestrates with marketing/storytelling agents for content, then builds visual screens in Pencil
code: MV
---

# Marketing Visual

Design landing pages, app store screenshots, pitch decks, and marketing presentations. Orchestrates with specialized marketing and storytelling agents for content strategy, then translates their output into polished visual designs in Pencil.

## What Success Looks Like

A complete set of marketing screens — landing page sections, App Store screenshots, or pitch slides — that tell a compelling story. Content comes from marketing agent expertise; visuals come from Pencil. The owner sees both the narrative and the design before any implementation starts.

## Orchestration Pattern

Pencil is a visual designer, not a copywriter. For marketing work, delegate content strategy to the right agent first:

### Available Marketing Agents

| Agent | Skill | Best For |
|---|---|---|
| Presentation Master | `bmad-cis-agent-presentation-master` | Pitch decks, investor presentations, keynote slides |
| Storyteller | `bmad-cis-agent-storyteller` | Brand narratives, app store copy, emotional hooks |
| Innovation Strategist | `bmad-cis-agent-innovation-strategist` | Positioning, competitive angle, value proposition |
| Freya (WDS) | `wds-agent-freya-ux` | UX-driven marketing, user journey storytelling |
| Product Brief | `bmad-product-brief` | Feature callouts, product one-pager content |

### Orchestration Flow

1. **Assess what's needed** — Does the owner have copy/content already, or do they need it generated?

2. **If content needed:** Spawn the appropriate marketing agent as a subagent. Provide context from MEMORY.md and project artifacts (WDS Brief, .impeccable.md). Ask for:
   - Key messages (max 5)
   - Hero headline + subhead
   - Feature callouts (name + one-line benefit)
   - Social proof / credibility elements
   - Call to action
   - Tone and audience

   Subagent returns compact JSON (max 500 tokens):
   ```json
   {
     "hero": {
       "headline": "Train smarter. Not harder.",
       "subhead": "AI-powered coaching that adapts to your body, not a generic plan.",
       "cta": "Start for free"
     },
     "features": [
       {"name": "Smart Check-ins", "benefit": "2-minute daily logs that adjust your program"},
       {"name": "Coach AI", "benefit": "Personalized insights based on your actual progress"}
     ],
     "social_proof": "10,000 athletes, 94% reach their goal",
     "tone": "confident, data-driven, approachable"
   }
   ```

3. **If content provided:** Skip to design phase directly.

## Design Patterns

### Landing Page Structure (Web — 1280px wide)

```javascript
// Hero Section
hero=I("document",{type:"frame",name:"Hero",width:1280,height:800,fill:"$bg",layout:"vertical",alignItems:"center",justifyContent:"center",gap:24})
I(hero,{type:"text",content:"[Headline]",fontFamily:"$display",fontSize:72,fontWeight:"800",letterSpacing:-2,fill:"$text-primary",textGrowth:"fixed-width",width:800,textAlign:"center"})
I(hero,{type:"text",content:"[Subhead]",fontFamily:"$body",fontSize:20,fontWeight:"400",fill:"$text-secondary",textGrowth:"fixed-width",width:600,textAlign:"center"})
ctas=I(hero,{type:"frame",layout:"horizontal",gap:16})
// Primary CTA:
cta=I(ctas,{type:"frame",cornerRadius:8,fill:"$text-primary",padding:[16,32],layout:"horizontal",alignItems:"center",justifyContent:"center"})
I(cta,{type:"text",content:"[CTA]",fontFamily:"$display",fontSize:18,fontWeight:"700",fill:"$bg"})
// Secondary CTA:
cta2=I(ctas,{type:"frame",cornerRadius:8,fill:"transparent",padding:[16,32],layout:"horizontal",alignItems:"center",justifyContent:"center"})
I(cta2,{type:"text",content:"See how it works",fontFamily:"$display",fontSize:18,fontWeight:"500",fill:"$text-primary"})
```

### Feature Card Grid

```javascript
grid=I(parent,{type:"frame",layout:"horizontal",width:"fill_container",gap:24,padding:[64,0]})
// Feature card:
card=I(grid,{type:"frame",layout:"vertical",width:"fill_container",cornerRadius:16,fill:"$surface",padding:32,gap:16})
I(card,{type:"icon_font",iconFontFamily:"lucide",iconFontName:"[icon]",width:32,height:32,fill:"$text-primary"})
I(card,{type:"text",content:"[Feature Name]",fontFamily:"$display",fontSize:20,fontWeight:"700",fill:"$text-primary"})
I(card,{type:"text",content:"[Benefit]",fontFamily:"$body",fontSize:15,fontWeight:"400",fill:"$text-secondary",textGrowth:"fixed-width",width:"fill_container",lineHeight:1.6})
```

### App Store Screenshots (Mobile — 402px)

Structure per screenshot:
- Background gradient or solid brand color
- Device frame or raw UI screenshot
- Bold headline at bottom
- Short supporting text

### Pitch Deck Slide (1920×1080)

```javascript
slide=I("document",{type:"frame",name:"Slide Title",width:1920,height:1080,fill:"$bg",layout:"none",clip:true})
```

Use `layout:"none"` for slides — positioning is intentional, not flow-based.

## Standard Landing Page Sections

Build these in order, each as a separate frame at the same x position, stacking vertically at 100px gaps:

1. **Hero** — headline, subhead, primary + secondary CTA, hero visual/screenshot
2. **Social Proof** — logos, numbers, testimonial quote
3. **Features** — 3-column grid with icon, name, benefit
4. **How It Works** — 3-step horizontal flow
5. **Screenshots** — product visuals in device frames or raw
6. **Pricing** — tiers or single CTA
7. **Final CTA** — repeated hero with different copy angle

## Platform Considerations

| Platform | Canvas Size | Key Constraints |
|---|---|---|
| Web landing page | 1280px wide | Sections stack vertically, design at desktop first |
| App Store screenshots | 402×874 (iOS) | Text must be legible at thumbnail size |
| Product Hunt | 1270×760 | Feature gallery images |
| Pitch deck | 1920×1080 | 16:9, readable from 10 feet |
| LinkedIn/Twitter card | 1200×628 | Single image, headline prominent |

## Memory Integration

After creating marketing visuals: note which marketing agent was used and the quality of their output in session log. Log successful content frameworks to BOND.md for future reference. If owner repeatedly uses a specific tone or headline style, note in patterns.

## After the Session

Log: which assets were created, which marketing agent was used, any notable content decisions. Update MEMORY.md with the product's positioning and messaging for future design sessions.
