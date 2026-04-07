---
name: pencil-patterns
description: Design screens, components, and iterate on existing designs in Pencil canvas
code: DP
---

# Design & Polish

Design new screens, build reusable components, and iterate on existing designs. Full Pencil MCP toolkit available:

| Tool | Purpose |
|------|---------|
| `batch_design` | Create/update/copy/replace/move/delete nodes (max 25 ops per call) |
| `batch_get` | Read nodes by ID or pattern, discover components |
| `get_screenshot` | Visual verification of a frame |
| `get_variables` / `set_variables` | Read and write design tokens |
| `find_empty_space_on_canvas` | Position new frames without overlap |
| `snapshot_layout` | Check layout structure, flag issues |
| `get_guidelines` | Load Pencil style guides |
| `export_nodes` | Export frames as PNG/JPEG/WEBP/PDF at any scale |
| `search_all_unique_properties` | Find all unique values for given properties across frames (used by audit, import, harvest) |
| `replace_all_matching_properties` | Bulk-update matching property values across frames (used by design system refactors) |
| `open_document` | Open or create .pen files |

Use what the task requires.

## What Success Looks Like

A screenshot the owner approves. Not a description of what you built — a visual they can see and react to. Every screen ends with `get_screenshot` and analysis before presenting. If the screenshot reveals issues, fix them first.

## Token Placeholders

Read DESIGN.md and BOND.md before designing. Map project tokens to these placeholders:

| Placeholder | Maps to |
|---|---|
| `$display` | Display font family |
| `$body` | Body font family |
| `$bg` | Background color |
| `$surface` | Surface/card color |
| `$text-primary` | Primary text |
| `$text-secondary` | Secondary text |
| `$text-tertiary` | Tertiary/hint text |
| `$border` | Borders/dividers |
| `$accent` | Accent color (if applicable) |

If token mappings exist in MEMORY.md, use those directly. Otherwise read DESIGN.md and derive them.

## Placeholder Workflow

Always use placeholder mode while constructing:
1. Create frame with `placeholder: true`
2. Build content sections
3. Update to `placeholder: false`
4. `get_screenshot` — analyze before presenting

## Mobile Frame Structure (402px)

```javascript
screen=I("document",{type:"frame",name:"Screen Name",width:402,height:874,fill:"$bg",clip:true,layout:"vertical",placeholder:true})
// Status bar — copy from existing: C("statusbar-id", screen, {})
content=I(screen,{type:"frame",layout:"vertical",width:"fill_container",height:"fill_container",gap:32,padding:[0,24,0,24]})
// Tab bar — copy from existing: C("tabbar-id", screen, {})
```

Position new screens with `find_empty_space_on_canvas({direction:"right", width:500, height:900, padding:100})`.

## Common UI Patterns

### Section Header
```javascript
hdr=I(parent,{type:"frame",layout:"horizontal",width:"fill_container",justifyContent:"space_between",alignItems:"center"})
I(hdr,{type:"text",content:"Title",fontFamily:"$display",fontSize:24,fontWeight:"800",letterSpacing:-0.5,fill:"$text-primary"})
I(hdr,{type:"text",content:"3/8",fontFamily:"$display",fontSize:24,fontWeight:"300",fill:"$text-secondary"})
```

### Label + Value Row
```javascript
row=I(parent,{type:"frame",layout:"horizontal",width:"fill_container",alignItems:"center",justifyContent:"space_between",padding:[16,0]})
I(row,{type:"text",content:"Label",fontFamily:"$display",fontSize:15,fontWeight:"600",fill:"$text-primary"})
I(row,{type:"text",content:"Value",fontFamily:"$display",fontSize:24,fontWeight:"800",fill:"$text-primary"})
```

### Icon + Label + Chevron Row
```javascript
row=I(parent,{type:"frame",layout:"horizontal",width:"fill_container",padding:16,alignItems:"center",justifyContent:"space_between"})
left=I(row,{type:"frame",layout:"horizontal",gap:12,alignItems:"center"})
I(left,{type:"icon_font",iconFontFamily:"lucide",iconFontName:"upload",width:18,height:18,fill:"$text-primary"})
I(left,{type:"text",content:"Label",fontFamily:"$display",fontSize:15,fontWeight:"600",fill:"$text-primary"})
I(row,{type:"icon_font",iconFontFamily:"lucide",iconFontName:"chevron-right",width:16,height:16,fill:"$text-tertiary"})
```

### Grouped List
```javascript
list=I(parent,{type:"frame",layout:"vertical",width:"fill_container",cornerRadius:16,fill:"$surface",gap:0})
// Dividers inside: I(list,{type:"rectangle",width:"fill_container",height:1,fill:"$border"})
```

### CTA Button
```javascript
btn=I(parent,{type:"frame",width:"fill_container",height:56,cornerRadius:20,fill:"$text-primary",layout:"horizontal",alignItems:"center",justifyContent:"center",gap:12})
I(btn,{type:"text",content:"Continue",fontFamily:"$display",fontSize:18,fontWeight:"800",fill:"$bg"})
I(btn,{type:"icon_font",iconFontFamily:"lucide",iconFontName:"arrow-right",width:20,height:20,fill:"$bg"})
```

### Segmented Control
```javascript
seg=I(parent,{type:"frame",layout:"horizontal",width:"fill_container",cornerRadius:24,fill:"$surface",height:48,padding:4,gap:4})
active=I(seg,{type:"frame",cornerRadius:20,fill:"$text-primary",width:"fill_container",height:"fill_container",layout:"vertical",alignItems:"center",justifyContent:"center"})
I(active,{type:"text",content:"Week",fontFamily:"$display",fontSize:14,fontWeight:"700",fill:"$bg"})
inactive=I(seg,{type:"frame",cornerRadius:20,width:"fill_container",height:"fill_container",layout:"vertical",alignItems:"center",justifyContent:"center"})
I(inactive,{type:"text",content:"Month",fontFamily:"$display",fontSize:14,fontWeight:"500",fill:"$text-secondary"})
```

### Metric Display
```javascript
metric=I(parent,{type:"frame",layout:"vertical",gap:4})
I(metric,{type:"text",content:"79.5",fontFamily:"$display",fontSize:48,fontWeight:"900",letterSpacing:-1,fill:"$text-primary"})
I(metric,{type:"text",content:"current kg",fontFamily:"$body",fontSize:13,fontWeight:"500",fill:"$text-tertiary"})
```

### Progress Bar
```javascript
bar=I(parent,{type:"frame",layout:"vertical",width:"fill_container",gap:6})
barHdr=I(bar,{type:"frame",layout:"horizontal",width:"fill_container",justifyContent:"space_between"})
I(barHdr,{type:"text",content:"Calories",fontFamily:"$display",fontSize:14,fontWeight:"600",fill:"$text-primary"})
I(barHdr,{type:"text",content:"88%",fontFamily:"$display",fontSize:14,fontWeight:"800",fill:"$text-primary"})
bg=I(bar,{type:"frame",width:"fill_container",height:8,cornerRadius:4,fill:"$surface",layout:"none"})
I(bg,{type:"rectangle",width:310,height:8,cornerRadius:4,fill:"$text-primary",x:0,y:0})
```

### Chat Bubbles
```javascript
// Received:
bubble=I(parent,{type:"frame",cornerRadius:20,fill:"$surface",padding:16,width:"fill_container"})
I(bubble,{type:"text",content:"Message",fontFamily:"$body",fontSize:14,fill:"$text-primary",textGrowth:"fixed-width",width:"fill_container",lineHeight:1.5})
// Sent (right-aligned):
wrap=I(parent,{type:"frame",width:"fill_container",alignItems:"end"})
sent=I(wrap,{type:"frame",cornerRadius:20,fill:"$text-primary",padding:16,width:280})
I(sent,{type:"text",content:"Message",fontFamily:"$body",fontSize:14,fill:"$bg",textGrowth:"fixed-width",width:"fill_container",lineHeight:1.5})
```

## Reusable Components

Create with `reusable: true`. Instance with `type: "ref"`. Override with `U(instance+"/child-id", {prop: value})`.

## Chrome Sharing

Copy status bar and tab bar from the first screen to all subsequent screens:
```javascript
C("statusbar-id", newScreen, {})
C("tabbar-id", newScreen, {})
```

## Constraints

- Max 25 `batch_design` operations per call — split larger screens into logical batches
- Always use `placeholder: true` while building, remove when done
- Check existing components with `batch_get({reusable: true})` before building new ones
- `snapshot_layout({problemsOnly: true})` after complex layouts to catch hidden issues

## Memory Integration

After designing: update `component-registry.md` for any new reusable components. Log approval/rejection patterns to session log. Note any notable design decisions (especially non-obvious ones) for distillation.

## After the Session

Capture in session log: screens built, components created, owner's design feedback, approval patterns observed.
