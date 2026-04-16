---
name: script-nodes
description: Generate programmable Pencil script nodes — data visualizations, gauges, charts, progress indicators, and custom interactive components
code: SN
---

# Script Nodes

Generate programmable visual components that render directly in the Pencil.dev canvas. Script nodes are JavaScript functions that return arrays of visual nodes — rectangles, text, paths, ellipses — with typed inputs that become UI controls in Pencil.

Use this for data-driven visuals that static frames can't express: charts, gauges, progress rings, clocks, visualizers, sparklines, and any component that needs computed geometry.

## What Success Looks Like

A working script node placed on the canvas with configurable inputs. The owner can adjust values (colors, data, sizes) directly in Pencil's properties panel without touching code. The visual updates live.

## Script Node Anatomy

Every script node follows this pattern:

```javascript
/**
 * @schema 2.10
 * @input label: string = "Progress"
 * @input value: number(min=0, max=100) = 75
 * @input accentColor: color = #FF7A00
 * @input trackColor: color = #E4E4E7
 */

const w = pencil.width;
const h = pencil.height;
const val = pencil.input.value;
const accent = pencil.input.accentColor;

const nodes = [];

// Background track
nodes.push({
  type: "rectangle",
  x: 0, y: h / 2 - 4,
  width: w, height: 8,
  cornerRadius: 4,
  fill: [{ type: "color", color: pencil.input.trackColor }]
});

// Progress fill
nodes.push({
  type: "rectangle",
  x: 0, y: h / 2 - 4,
  width: w * (val / 100), height: 8,
  cornerRadius: 4,
  fill: [{ type: "color", color: accent }]
});

// Label
nodes.push({
  type: "text",
  x: 0, y: 0,
  width: w, height: 24,
  content: `${pencil.input.label}: ${val}%`,
  fontSize: 14,
  fontFamily: "$body",
  fill: [{ type: "color", color: "#18181B" }]
});

return nodes;
```

## Input Types

```javascript
@input name: string = "default"           // Text field
@input count: number = 10                  // Number field
@input count: number(min=1, max=100) = 50  // Number with range
@input accent: color = #FF7A00            // Color picker
```

Inputs appear as editable properties in Pencil's panel. Changing them re-renders the script node live.

## Node Types

| Type | Properties | Use for |
|---|---|---|
| `rectangle` | x, y, width, height, cornerRadius, fill, stroke, rotation, opacity | Bars, backgrounds, cards, tracks |
| `text` | x, y, width, height, content, fontSize, fontFamily, fontWeight, textAlign, fill | Labels, values, annotations |
| `ellipse` | x, y, width, height, fill, stroke | Dots, circles, ring segments |
| `path` | x, y, width, height, viewBox, geometry (SVG path), fill, stroke | Arcs, custom shapes, icons |
| `ref` | refId, x, y, rotation | Instances of reusable components |

## Fill & Stroke

```javascript
// Solid color
fill: [{ type: "color", color: "#FF7A00" }]

// Use Pencil variable
fill: [{ type: "color", color: "$accent" }]

// Linear gradient
fill: [{
  type: "gradient",
  gradientType: "linear",
  rotation: 90,
  colors: [
    { position: 0, color: "#FF7A00" },
    { position: 1, color: "#FF4500" }
  ]
}]

// Stroke
stroke: {
  align: "center",
  thickness: 2,
  fill: [{ type: "color", color: "$border" }]
}
```

## Effects

```javascript
effect: {
  type: "shadow",
  color: "#00000020",
  x: 0, y: 4,
  blur: 12,
  spread: 0
}
```

## Common Script Node Patterns

### Progress Ring

```javascript
/**
 * @schema 2.10
 * @input value: number(min=0, max=100) = 72
 * @input size: number = 120
 * @input thickness: number = 8
 * @input accent: color = #FF7A00
 * @input track: color = #E4E4E7
 */

const cx = pencil.width / 2;
const cy = pencil.height / 2;
const r = pencil.input.size / 2 - pencil.input.thickness;
const pct = pencil.input.value / 100;
const angle = pct * 360;

// SVG arc path for the progress
const rad = (a) => (a - 90) * Math.PI / 180;
const endX = cx + r * Math.cos(rad(angle));
const endY = cy + r * Math.sin(rad(angle));
const largeArc = angle > 180 ? 1 : 0;
const startX = cx + r * Math.cos(rad(0));
const startY = cy + r * Math.sin(rad(0));

return [
  // Track circle
  { type: "ellipse", x: cx - r, y: cy - r, width: r * 2, height: r * 2,
    stroke: { align: "center", thickness: pencil.input.thickness,
    fill: [{ type: "color", color: pencil.input.track }] } },
  // Progress arc
  { type: "path", x: 0, y: 0, width: pencil.width, height: pencil.height,
    viewBox: `0 0 ${pencil.width} ${pencil.height}`,
    geometry: `M ${startX} ${startY} A ${r} ${r} 0 ${largeArc} 1 ${endX} ${endY}`,
    stroke: { align: "center", thickness: pencil.input.thickness,
    fill: [{ type: "color", color: pencil.input.accent }] } },
  // Value text
  { type: "text", x: 0, y: cy - 16, width: pencil.width, height: 32,
    content: `${pencil.input.value}%`, fontSize: 28, fontWeight: "800",
    fontFamily: "$display", textAlign: "center",
    fill: [{ type: "color", color: "#18181B" }] }
];
```

### Bar Chart

```javascript
/**
 * @schema 2.10
 * @input data: string = "Mon:65,Tue:80,Wed:45,Thu:90,Fri:70,Sat:55,Sun:85"
 * @input barColor: color = #FF7A00
 * @input labelColor: color = #71717A
 */

const entries = pencil.input.data.split(",").map(e => {
  const [label, val] = e.split(":");
  return { label, value: Number(val) };
});

const maxVal = Math.max(...entries.map(e => e.value));
const barW = (pencil.width - (entries.length + 1) * 8) / entries.length;
const chartH = pencil.height - 32;
const nodes = [];

entries.forEach((entry, i) => {
  const x = 8 + i * (barW + 8);
  const h = (entry.value / maxVal) * chartH;
  const y = chartH - h;

  // Bar
  nodes.push({
    type: "rectangle", x, y, width: barW, height: h,
    cornerRadius: 4,
    fill: [{ type: "color", color: pencil.input.barColor }]
  });

  // Label
  nodes.push({
    type: "text", x, y: chartH + 4, width: barW, height: 24,
    content: entry.label, fontSize: 11, fontWeight: "500",
    fontFamily: "$body", textAlign: "center",
    fill: [{ type: "color", color: pencil.input.labelColor }]
  });
});

return nodes;
```

### Sparkline

```javascript
/**
 * @schema 2.10
 * @input data: string = "65,80,45,90,70,55,85,60,75,95"
 * @input lineColor: color = #FF7A00
 * @input fillOpacity: number(min=0, max=1) = 0.1
 */

const values = pencil.input.data.split(",").map(Number);
const max = Math.max(...values);
const min = Math.min(...values);
const range = max - min || 1;
const w = pencil.width;
const h = pencil.height;
const step = w / (values.length - 1);

let linePath = "";
let fillPath = `M 0 ${h}`;

values.forEach((v, i) => {
  const x = i * step;
  const y = h - ((v - min) / range) * h;
  linePath += `${i === 0 ? "M" : "L"} ${x} ${y} `;
  fillPath += ` L ${x} ${y}`;
});
fillPath += ` L ${w} ${h} Z`;

return [
  // Fill area
  { type: "path", x: 0, y: 0, width: w, height: h,
    viewBox: `0 0 ${w} ${h}`, geometry: fillPath,
    fill: [{ type: "color", color: pencil.input.lineColor }],
    opacity: pencil.input.fillOpacity },
  // Line
  { type: "path", x: 0, y: 0, width: w, height: h,
    viewBox: `0 0 ${w} ${h}`, geometry: linePath,
    stroke: { align: "center", thickness: 2,
    fill: [{ type: "color", color: pencil.input.lineColor }] } }
];
```

## Workflow

1. **Understand the need** — what data visualization or dynamic component does the owner want?
2. **Choose the pattern** — progress ring, bar chart, sparkline, gauge, or custom
3. **Write the script** — follow the @schema 2.10 pattern with typed @input declarations
4. **Place on canvas** — create a script node frame in Pencil with the script content
5. **Configure inputs** — set the default values to match the design context
6. **Screenshot + verify** — does it look right? Adjust dimensions, colors, spacing

## When to Use Script Nodes vs Static Frames

| Use Script Nodes | Use Static Frames |
|---|---|
| Data changes (charts, metrics, progress) | Fixed UI (headers, navigation, forms) |
| Computed geometry (arcs, paths, radial) | Layout-based composition (stacks, grids) |
| Configurable components (color/size inputs) | Pixel-perfect branded elements |
| Repeating patterns driven by data | One-off illustrations or graphics |

## Token Integration

Script nodes can reference Pencil variables using the `$` prefix in color values:

```javascript
fill: [{ type: "color", color: "$accent" }]
fill: [{ type: "color", color: "$text-primary" }]
```

This keeps script nodes in sync with the design system. When tokens change, script nodes update automatically.

## Memory Integration

Store commonly requested script node types in session log. After 3+ sessions creating similar nodes, suggest adding a script template to MEMORY.md for faster generation.

## After the Session

Log: which script nodes were created, what data they visualize, any reusable patterns discovered.
