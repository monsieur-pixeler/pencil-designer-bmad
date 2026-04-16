---
name: re-capture-ios-device
description: "Sub-reference for [RE] — iOS device capture via AirPlay/QuickTime"
parent: reverse-engineer
---

# iOS/iPad Device Capture via AirPlay — Guided

**Setup instructions for the user:**

> 1. Open **QuickTime Player** on your Mac
> 2. File → New Movie Recording
> 3. Click the dropdown arrow next to the record button → select your iPhone/iPad
> 4. Your device screen is now mirrored in QuickTime
> 5. Keep the QuickTime window visible — I'll capture from it

**Or with AirPlay (macOS Monterey+):**

> 1. On your iPhone: open Control Center → Screen Mirroring → select your Mac
> 2. Your phone screen appears in a window on your Mac
> 3. Keep it visible — I'll capture from it

**Guided navigation:**

The system drives the process step by step:

```
"Navigate to the main/home screen and say 'ready'."
→ user says "ready"
→ screencapture -x /tmp/re-capture/01-home.png
→ "Got it. Now open the settings or profile screen."
→ user says "ready"
→ screencapture -x /tmp/re-capture/02-settings.png
→ "Good. Now open any list or detail view."
...
```

**Smart prompting — ask about the app structure first:**

Before capturing, ask: "Describe the main sections of the app — how many tabs, what are the key screens?" This lets the system create a capture plan:

```
Capture plan for [App Name]:
  1. [ ] Tab 1: Dashboard / Home
  2. [ ] Tab 2: History / Feed
  3. [ ] Tab 3: Add / Create
  4. [ ] Tab 4: Profile / Settings
  5. [ ] Key detail screen (from tab 1)
  6. [ ] Any modal / sheet
  7. [ ] Empty state (if accessible)
  8. [ ] Dark mode (if available — toggle in Control Center)
```

Check off each as captured. Announce progress: "4 of 8 screens captured. Next: open the Profile tab."

**Auto-mode option:**

```
"Want me to capture automatically every 3 seconds while you navigate?
Just swipe through the app naturally — I'll sort out the duplicates."
```

Then use `screencapture` in a timed loop, deduplicate after.
