#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Calculate WCAG contrast ratio between two colors.

Outputs JSON with ratio, WCAG AA and AAA pass/fail for normal and large text.

Usage:
    python3 contrast-ratio.py --fg "#000000" --bg "#FFFFFF"
    python3 contrast-ratio.py --fg "#71717A" --bg "#F4F4F5" --context "hint text on surface"
"""

import argparse
import json
import sys


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Parse a hex color string to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 3:
        hex_color = "".join(c * 2 for c in hex_color)
    return int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)


def linearize(channel: int) -> float:
    """Convert sRGB channel (0-255) to linear light value."""
    c = channel / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    """Calculate WCAG relative luminance for a hex color."""
    r, g, b = hex_to_rgb(hex_color)
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def contrast_ratio(fg: str, bg: str) -> float:
    """Calculate WCAG contrast ratio between foreground and background."""
    l1 = relative_luminance(fg)
    l2 = relative_luminance(bg)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate WCAG contrast ratio between two colors"
    )
    parser.add_argument("--fg", required=True, help="Foreground color (hex, e.g. #000000)")
    parser.add_argument("--bg", required=True, help="Background color (hex, e.g. #FFFFFF)")
    parser.add_argument("--context", default="", help="Optional context label (e.g. 'hint text on surface')")
    args = parser.parse_args()

    try:
        ratio = contrast_ratio(args.fg, args.bg)
    except ValueError as e:
        print(json.dumps({"status": "error", "message": str(e)}))
        sys.exit(2)

    result = {
        "fg": args.fg,
        "bg": args.bg,
        "context": args.context,
        "ratio": round(ratio, 2),
        "wcag": {
            "AA_normal_text": ratio >= 4.5,    # body text, UI components
            "AA_large_text": ratio >= 3.0,     # 18px+ or 14px+ bold
            "AAA_normal_text": ratio >= 7.0,   # enhanced accessibility
            "AAA_large_text": ratio >= 4.5,
            "non_text_minimum": ratio >= 3.0,  # borders, icons, UI components
        },
        "verdict": (
            "AAA" if ratio >= 7.0
            else "AA" if ratio >= 4.5
            else "AA (large text only)" if ratio >= 3.0
            else "FAIL"
        ),
        "suggestion": None,
    }

    # Generate fix suggestion if failing
    if ratio < 4.5:
        result["suggestion"] = (
            f"Ratio {ratio:.2f}:1 — below AA (4.5:1) for normal text. "
            f"Darken the foreground or lighten the background for text on this surface."
        )
    elif ratio < 7.0:
        result["suggestion"] = (
            f"Ratio {ratio:.2f}:1 — passes AA but not AAA (7:1). "
            f"Acceptable for body text; consider higher contrast for critical content."
        )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
