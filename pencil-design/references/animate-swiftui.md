---
name: animate-swiftui
description: "Sub-reference for [AN] Animate — SwiftUI animation modifier chain generation"
parent: animate
---

# SwiftUI Animations — SwiftUI Animation Reference

Sub-reference of `[AN] Animate`. Loaded when the project framework is SwiftUI.

Covers entrance animations, navigation transitions, interactive feedback, matched geometry effects, and phase-based sequences.
3. **Generate SwiftUI code** — `.animation()`, `withAnimation {}`, `matchedGeometryEffect`, or `PhaseAnimator` as appropriate
4. **Annotate the Pencil frame** — add annotation nodes to mark animated elements and their properties

## Animation Categories

### Entrance Animations (View Appear / onAppear)

```swift
// Fade up — standard entrance for content sections
struct FadeUpModifier: ViewModifier {
    @State private var appeared = false

    func body(content: Content) -> some View {
        content
            .opacity(appeared ? 1 : 0)
            .offset(y: appeared ? 0 : 20)
            .onAppear {
                withAnimation(.spring(response: 0.4, dampingFraction: 0.8)) {
                    appeared = true
                }
            }
    }
}

// Stagger children — for lists, grids, feature cards
ForEach(items.indices, id: \.self) { index in
    ItemView(item: items[index])
        .opacity(appeared ? 1 : 0)
        .offset(y: appeared ? 0 : 16)
        .animation(
            .spring(response: 0.4, dampingFraction: 0.8)
            .delay(Double(index) * 0.08),
            value: appeared
        )
}
```

### Navigation Transitions

```swift
// Push transition (NavigationStack default — customize if needed)
.navigationTransition(.slide)

// Sheet entrance
.sheet(isPresented: $showSheet) {
    SheetView()
        .presentationDetents([.medium, .large])
        .presentationDragIndicator(.visible)
}

// Full-screen cover with custom animation
.fullScreenCover(isPresented: $showFull) {
    FullView()
}
// iOS 17+: custom transition on full-screen cover
.transition(.move(edge: .bottom).combined(with: .opacity))
```

### Interactive Feedback (Buttons, Gestures)

```swift
// Button press feel — scale down on tap
Button(action: {}) {
    Label("Continue", systemImage: "arrow.right")
}
.buttonStyle(ScaleButtonStyle())

struct ScaleButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.97 : 1.0)
            .animation(.spring(response: 0.2, dampingFraction: 0.6), value: configuration.isPressed)
    }
}

// Card lift on hover (iPadOS / macOS)
.hoverEffect(.lift)

// Swipe gesture
.gesture(
    DragGesture()
        .onChanged { value in dragOffset = value.translation }
        .onEnded { value in
            withAnimation(.spring(response: 0.3, dampingFraction: 0.7)) {
                dragOffset = value.translation.width > 80 ? .init(width: 400, height: 0) : .zero
            }
        }
)
```

### Matched Geometry Effect (Shared Element Transitions)

```swift
@Namespace private var heroNamespace

// Source view
Image(thumbnail)
    .matchedGeometryEffect(id: "hero-\(item.id)", in: heroNamespace)

// Destination view
Image(fullSize)
    .matchedGeometryEffect(id: "hero-\(item.id)", in: heroNamespace)
```

### Phase Animator (iOS 17+, multi-step sequences)

```swift
// Animated icon sequence (success state, loading, celebration)
PhaseAnimator([Phase.idle, .success, .rest]) { phase in
    CheckmarkView(phase: phase)
} animation: { phase in
    switch phase {
    case .idle: .spring(response: 0.3, dampingFraction: 0.7)
    case .success: .spring(response: 0.4, dampingFraction: 0.5)
    case .rest: .easeOut(duration: 0.3)
    }
}
```

### Progress / Counter Animations

```swift
// Animated number counter
struct AnimatedCounter: View {
    let value: Double
    @State private var displayed: Double = 0

    var body: some View {
        Text(displayed, format: .number.precision(.fractionLength(0)))
            .contentTransition(.numericText(value: displayed))
            .onAppear {
                withAnimation(.spring(response: 0.8, dampingFraction: 0.7)) {
                    displayed = value
                }
            }
    }
}

// Progress bar
RoundedRectangle(cornerRadius: 4)
    .fill(Color.accentColor)
    .frame(width: geometry.size.width * progress)
    .animation(.spring(response: 0.6, dampingFraction: 0.8), value: progress)
```

### Layout Animations (Expand / Collapse)

```swift
// Expanding section
DisclosureGroup(isExpanded: $expanded) {
    content
        .transition(.opacity.combined(with: .move(edge: .top)))
} label: {
    Label("Section title", systemImage: "chevron.right")
        .rotationEffect(.degrees(expanded ? 90 : 0))
        .animation(.spring(response: 0.3, dampingFraction: 0.7), value: expanded)
}
.animation(.spring(response: 0.3, dampingFraction: 0.7), value: expanded)
```

## Annotating Pencil Designs

For each animated element, add an annotation frame next to it using the project's annotation color from BOND.md. If no annotation color is defined, use the $accent variable:

```javascript
// Read annotation color from variables first
anno=I(parent,{type:"frame",cornerRadius:4,fill:"$annotation-animation",padding:[4,8],layout:"horizontal",gap:4})
I(anno,{type:"text",content:"SA",fontFamily:"$body",fontSize:10,fontWeight:"700",fill:"#FFFFFF"})
I(anno,{type:"text",content:"fade-up 0.4s spring",fontFamily:"$body",fontSize:10,fill:"#FFFFFF",opacity:0.7})
```

Define `$annotation-animation` in the .pen file variables if it doesn't exist. Suggest a color that contrasts with both design notes and Framer Motion annotations.

## Animation Decision Framework

| Element Type | SwiftUI Approach |
|---|---|
| Screen / view entrance | `.onAppear` + `withAnimation(.spring(...))` |
| Hero / headline | Fade up, delay 0s |
| Supporting content | Fade up, delay 0.1–0.2s |
| CTA button | Fade up, delay + `ScaleButtonStyle` |
| List / grid items | Stagger `.animation(...delay:)` |
| Navigation push | `.navigationTransition(.slide)` |
| Sheet presentation | `.sheet` default (or custom `.transition`) |
| Matched element (gallery → detail) | `matchedGeometryEffect` |
| Multi-step sequence | `PhaseAnimator` (iOS 17+) |
| Number / stat | `contentTransition(.numericText)` |
| Progress bar | `.animation` on frame width |
| Toggle / checkbox | `withAnimation(.spring(response:0.2))` |
| Tab switch | `TabView` default or custom indicator animation |

## Spring Presets

```swift
// Snappy — buttons, toggles, interactive elements
.spring(response: 0.2, dampingFraction: 0.6)

// Standard — content entrances, list items
.spring(response: 0.4, dampingFraction: 0.8)

// Smooth — page-level transitions, sheets
.spring(response: 0.5, dampingFraction: 0.9)

// Bouncy — success states, gamification, celebrations
.spring(response: 0.4, dampingFraction: 0.5)

// Gentle — decorative, background elements
.easeOut(duration: 0.5)
```

## Full Screen Animation Spec

When annotating a complete screen, generate a spec alongside the code:

```
Screen: Dashboard
Framework: SwiftUI

Animations:
  Header        — .onAppear fade + slide up (y:20→0, 0.3s spring), delay 0
  Metric cards  — stagger .onAppear, 0.08s between, starting delay 0.1s
  CTA button    — .onAppear fade + slide (0.4s), ScaleButtonStyle on press
  Tab indicator — withAnimation(.spring(response:0.2)) on selection change

Transitions:
  Push to detail — .navigationTransition(.slide) (default)
  Metric → chart — matchedGeometryEffect on metric value
```

## After the Session

Follow the standard session close protocol. Additionally log: which screens received SwiftUI animation specs, which patterns were used, animation preferences revealed.
