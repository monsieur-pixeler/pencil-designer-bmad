---
name: re-capture-macos
description: "Sub-reference for [RE] — macOS app capture via window capture + Accessibility"
parent: reverse-engineer
---

# macOS App Capture — Semi-Automated

macOS apps can be captured per-window and inspected via Accessibility APIs.

**Step 1 — Find the app window:**

```bash
# List all windows with their IDs (for targeted capture)
osascript -e 'tell application "System Events" to get {name, id} of every window of every process whose visible is true'

# Or find a specific app:
osascript -e 'tell application "System Events" to get id of every window of process "[App Name]"'
```

**Step 2 — Capture the window:**

```bash
# Capture a specific window by ID (no shadow, no desktop)
screencapture -l <windowID> -o /tmp/re-capture/01-main.png

# Or interactive: let user click the window
screencapture -w -o /tmp/re-capture/01-main.png
```

**Step 3 — Accessibility inspection (optional, powerful):**

macOS Accessibility APIs expose the entire UI tree — labels, roles, frames, values:

```bash
# Dump the accessibility tree of the frontmost app
python3 -c "
import subprocess, json
result = subprocess.run(
    ['osascript', '-e', '''
    tell application \"System Events\"
        set frontApp to first application process whose frontmost is true
        set appName to name of frontApp
        set winList to {}
        repeat with w in windows of frontApp
            set winInfo to {name of w, position of w, size of w}
            set end of winList to winInfo
        end repeat
        return {appName, winList}
    end tell
    '''],
    capture_output=True, text=True
)
print(result.stdout)
"
```

This gives us actual element positions and sizes — more accurate than pixel-guessing for layout extraction.

**Step 4 — Guided navigation for multiple states:**

Mac apps often have multiple view states in one window (sidebar selections, tabs, inspectors). Guide the user:

```
"Click on each sidebar item and say 'ready' — I'll capture each state."
"Open the preferences window and say 'ready'."
"Resize the window to minimum width and say 'ready' — I'll check the compact layout."
```

**Step 5 — Window chrome detection:**

macOS windows have standard chrome (title bar, toolbar, sidebar). Detect:
- **Title bar:** Standard (28px) or tall toolbar style
- **Sidebar:** NavigationSplitView pattern (detect from width ratio)
- **Tab bar:** Segmented control in toolbar or tab view
- **Inspector:** Right-side panel (if window has three columns)

Map these to NavigationSplitView / HSplitView patterns for macOS rebuild.

## Platform Tips — macOS Window Patterns

- Standard title bar: 28px. Toolbar: 38-52px depending on style
- Sidebar width: typically 200-280px (NavigationSplitView default: 240px)
- Three-column layout: sidebar (240) + content (flexible) + inspector (260-300)
- macOS uses pointer-sized targets (smaller than iOS 44pt minimum)
- Menu bar: not part of the window — capture separately if menu structure matters
- Sheets: slide down from toolbar, not from bottom like iOS
- Popovers: common for settings/options — capture these as separate states
- Use `NSWindow.contentLayoutRect` via Accessibility to get exact content area bounds
