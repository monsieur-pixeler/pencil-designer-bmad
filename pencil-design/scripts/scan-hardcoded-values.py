#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Scan source files for hardcoded design values that should be tokens.

Detects hex colors, hardcoded font names, and magic spacing numbers
in Swift/TypeScript/CSS source files that match known design token values.

Usage:
    python3 scan-hardcoded-values.py {project-root}/src
    python3 scan-hardcoded-values.py {project-root}/RippedBodyCoach --extensions .swift
    python3 scan-hardcoded-values.py {project-root}/src --token-map tokens.json
"""

import argparse
import json
import re
import sys
from pathlib import Path


# Default token patterns to scan for
DEFAULT_TOKENS = {
    "colors": {
        "#000000": "color.text.primary",
        "#FFFFFF": "color.bg",
        "#F4F4F5": "color.surface",
        "#E4E4E7": "color.border",
        "#A1A1AA": "color.text.tertiary",
        "#71717A": "color.text.secondary",
        "#27272A": "color.surface.dark",
    },
    "fonts": {
        '"Outfit"': "font.display",
        '"Inter"': "font.body",
        "Outfit": "font.display",
        "Inter": "font.body",
    },
}

# Regex patterns for hardcoded values
HEX_COLOR_RE = re.compile(r'#([0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b')
FONT_NAME_RE = re.compile(r'["\']?(Outfit|Inter|SF Pro|Helvetica)["\']?')

SUPPORTED_EXTENSIONS = {".swift", ".ts", ".tsx", ".css", ".scss", ".js", ".jsx"}


def scan_file(file_path: Path, known_tokens: dict) -> list[dict]:
    """Scan a single file for hardcoded design values."""
    findings = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings

    lines = content.split("\n")
    for line_num, line in enumerate(lines, 1):
        # Skip comments
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("#"):
            continue

        # Check hex colors
        for match in HEX_COLOR_RE.finditer(line):
            hex_val = "#" + match.group(1).upper()
            # Normalize 3-char hex to 6-char
            if len(match.group(1)) == 3:
                hex_val = "#" + "".join(c * 2 for c in match.group(1).upper())

            if hex_val in known_tokens["colors"]:
                findings.append({
                    "file": str(file_path),
                    "line": line_num,
                    "type": "hardcoded_color",
                    "value": hex_val,
                    "token": known_tokens["colors"][hex_val],
                    "context": stripped[:80],
                    "severity": "medium",
                })

        # Check font names
        for match in FONT_NAME_RE.finditer(line):
            font = match.group(1)
            for pattern, token in known_tokens["fonts"].items():
                if font in pattern:
                    findings.append({
                        "file": str(file_path),
                        "line": line_num,
                        "type": "hardcoded_font",
                        "value": font,
                        "token": token,
                        "context": stripped[:80],
                        "severity": "low",
                    })
                    break

    return findings


def main():
    parser = argparse.ArgumentParser(
        description="Scan source files for hardcoded design values that should be tokens"
    )
    parser.add_argument("source_dir", help="Directory to scan")
    parser.add_argument(
        "--extensions",
        help="Comma-separated file extensions to scan (default: .swift,.ts,.tsx,.css)",
        default=",".join(SUPPORTED_EXTENSIONS),
    )
    parser.add_argument(
        "--token-map",
        help="JSON file with custom token mappings {colors: {hex: token}, fonts: {name: token}}",
        default=None,
    )
    args = parser.parse_args()

    source_dir = Path(args.source_dir)
    if not source_dir.exists():
        print(json.dumps({"status": "error", "message": f"Directory not found: {source_dir}"}))
        sys.exit(2)

    extensions = {ext.strip() for ext in args.extensions.split(",")}

    # Load token map
    known_tokens = DEFAULT_TOKENS.copy()
    if args.token_map:
        token_map_path = Path(args.token_map)
        if token_map_path.exists():
            custom = json.loads(token_map_path.read_text())
            known_tokens["colors"].update(custom.get("colors", {}))
            known_tokens["fonts"].update(custom.get("fonts", {}))

    # Scan files
    all_findings = []
    files_scanned = 0

    for file_path in sorted(source_dir.rglob("*")):
        if file_path.is_file() and file_path.suffix.lower() in extensions:
            # Skip node_modules, .git, build artifacts
            parts = file_path.parts
            if any(p in parts for p in ("node_modules", ".git", "dist", "build", "DerivedData")):
                continue
            findings = scan_file(file_path, known_tokens)
            all_findings.extend(findings)
            files_scanned += 1

    # Deduplicate (same file+line+value)
    seen = set()
    deduped = []
    for f in all_findings:
        key = (f["file"], f["line"], f["value"])
        if key not in seen:
            seen.add(key)
            deduped.append(f)

    by_severity = {"medium": 0, "low": 0, "high": 0}
    for f in deduped:
        by_severity[f.get("severity", "low")] += 1

    result = {
        "status": "pass" if not deduped else "warning",
        "source_dir": str(source_dir),
        "files_scanned": files_scanned,
        "findings": deduped,
        "summary": {
            "total": len(deduped),
            "by_severity": by_severity,
            "by_type": {
                "hardcoded_color": sum(1 for f in deduped if f["type"] == "hardcoded_color"),
                "hardcoded_font": sum(1 for f in deduped if f["type"] == "hardcoded_font"),
            },
        },
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
