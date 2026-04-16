---
name: re-capture-ios-sim
description: "Sub-reference for [RE] — iOS Simulator capture via xcrun simctl"
parent: reverse-engineer
---

# iOS Simulator Capture — Fully Automated

**Step 1 — Boot and launch:**

```bash
# List available simulators
xcrun simctl list devices available | grep -E "iPhone|iPad"

# Boot if needed
xcrun simctl boot "iPhone 16 Pro"

# Launch the target app (user provides bundle ID or app name)
xcrun simctl launch booted com.example.app
```

**Step 2 — Guided capture with auto-screenshot:**

Announce: "I'll take screenshots as you navigate. Tell me when you've reached each screen, or I'll capture every 3 seconds if you prefer auto-mode."

```bash
# Single screenshot
xcrun simctl io booted screenshot /tmp/re-capture/screen-001.png

# Or timed burst (auto-mode):
# Take a screenshot every 3 seconds for N seconds
for i in $(seq 1 20); do
  xcrun simctl io booted screenshot "/tmp/re-capture/screen-$(printf '%03d' $i).png"
  sleep 3
done
```

**Step 3 — Deduplicate:**

After auto-capture, compare sequential screenshots to remove duplicates (user was idle on the same screen). Use image comparison:

```bash
# Quick pixel diff — if images are identical or near-identical, skip
python3 -c "
from pathlib import Path
import hashlib
seen = {}
for f in sorted(Path('/tmp/re-capture').glob('*.png')):
    h = hashlib.md5(f.read_bytes()).hexdigest()
    if h in seen: f.unlink()
    else: seen[h] = f
print(f'Kept {len(seen)} unique screens')
"
```

## Platform Tips — iOS System Conventions

- SF Pro is the system font — don't extract it as a custom font, map to iOS text styles
- Tab bar is 49px, nav bar is 44px (large title: 96px) — use standard heights
- Safe area: 59px top (Dynamic Island), 34px bottom (home indicator)
- Pull-to-refresh, swipe-to-delete — note interaction patterns, not just visuals
