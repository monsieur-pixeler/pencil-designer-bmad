#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Extract design token definitions from DESIGN.md (or similar markdown) to JSON.

Reads a markdown design system file and extracts all token definitions:
color hex values, font names, spacing/sizing values. Outputs JSON consumable
by other scripts (diff-tokens.py, classify-token-drift.py).

Usage:
    python3 design-token-extractor.py --input DESIGN.md
    python3 design-token-extractor.py --input DESIGN.md --output tokens.json
    python3 design-token-extractor.py --input DESIGN.md --format pencil

Exit codes: 0=tokens found, 1=no tokens found, 2=error
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Patterns for extracting tokens from markdown
HEX_COLOR_RE = re.compile(
    r'[`*]*\$?([\w-]+)[`*]*\s*[:=→\-|]+\s*[`*]*([#][0-9A-Fa-f]{3,8})[`*]*',
)

# Match color names with hex: "Background: #FFFFFF" or "| bg | #FFFFFF |"
NAMED_COLOR_RE = re.compile(
    r'(?:^|\|)\s*[`*]*([\w\s-]+?)[`*]*\s*(?:\||:|\s→\s)\s*[`*]*([#][0-9A-Fa-f]{3,8})[`*]*',
    re.MULTILINE,
)

# Font family extraction: "Font: Inter" or "Display: Outfit 800"
FONT_RE = re.compile(
    r'(?:font|typeface|family|display|heading|body|caption|label|mono)\s*[:=→|]+\s*[`*]*([\w\s]+?)[`*]*(?:\s*[(/]|\s*\d|\s*$)',
    re.IGNORECASE | re.MULTILINE,
)

# Spacing/sizing values: "$space-2: 8px" or "| space2 | 8 |"
SPACING_RE = re.compile(
    r'[`*]*\$?(space|spacing|gap|padding|margin|radius|corner|size)[-_]?([\w]*)[`*]*\s*[:=→|]+\s*[`*]*(\d+(?:\.\d+)?)\s*(?:px|pt|dp)?[`*]*',
    re.IGNORECASE,
)

# Generic key-value in markdown tables: "| token-name | value |"
TABLE_ROW_RE = re.compile(
    r'\|\s*[`*]*([\w.-]+)[`*]*\s*\|\s*[`*]*([^|]+?)[`*]*\s*\|',
)


def normalize_hex(value: str) -> str | None:
    """Normalize a hex color value to uppercase 6-char format."""
    value = value.strip().lstrip('#')
    if re.match(r'^[0-9A-Fa-f]{3}$', value):
        value = ''.join(c * 2 for c in value)
    if re.match(r'^[0-9A-Fa-f]{6}$', value):
        return '#' + value.upper()
    if re.match(r'^[0-9A-Fa-f]{8}$', value):
        return '#' + value[:6].upper()
    return None


def normalize_token_name(name: str) -> str:
    """Normalize a token name to lowercase kebab-case."""
    name = name.strip().lower()
    name = re.sub(r'[\s_]+', '-', name)
    name = re.sub(r'[^a-z0-9-]', '', name)
    return name.strip('-')


def extract_colors(content: str) -> dict[str, str]:
    """Extract color tokens from markdown content."""
    colors = {}

    for match in HEX_COLOR_RE.finditer(content):
        name = normalize_token_name(match.group(1))
        hex_val = normalize_hex(match.group(2))
        if name and hex_val:
            colors[name] = hex_val

    for match in NAMED_COLOR_RE.finditer(content):
        name = normalize_token_name(match.group(1))
        hex_val = normalize_hex(match.group(2))
        if name and hex_val and len(name) > 1:
            colors[name] = hex_val

    return colors


def extract_fonts(content: str) -> list[str]:
    """Extract font family names from markdown content."""
    fonts = set()
    for match in FONT_RE.finditer(content):
        font = match.group(1).strip()
        # Filter out common false positives
        if font.lower() not in ('the', 'a', 'an', 'or', 'and', 'is', 'are', 'use', 'used'):
            fonts.add(font)
    return sorted(fonts)


def extract_spacing(content: str) -> dict[str, float]:
    """Extract spacing/sizing tokens from markdown content."""
    spacing = {}
    for match in SPACING_RE.finditer(content):
        category = match.group(1).lower()
        suffix = match.group(2) or ''
        value = float(match.group(3))
        name = f'{category}-{suffix}'.rstrip('-') if suffix else category
        spacing[normalize_token_name(name)] = value
    return spacing


def to_pencil_format(colors: dict, fonts: list, spacing: dict) -> list[dict]:
    """Convert extracted tokens to Pencil get_variables compatible format."""
    variables = []
    for name, hex_val in colors.items():
        variables.append({
            'name': name,
            'value': hex_val,
            'type': 'color',
        })
    for name, value in spacing.items():
        variables.append({
            'name': name,
            'value': str(value),
            'type': 'number',
        })
    return variables


def main():
    parser = argparse.ArgumentParser(
        description='Extract design tokens from DESIGN.md to JSON'
    )
    parser.add_argument('--input', required=True,
                        help='Path to DESIGN.md or similar markdown design system file')
    parser.add_argument('--output',
                        help='Write JSON result to file instead of stdout')
    parser.add_argument('--format', choices=['standard', 'pencil'],
                        default='standard',
                        help='Output format: standard (grouped) or pencil (get_variables compatible)')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(json.dumps({'status': 'error', 'message': f'File not found: {input_path}'}))
        sys.exit(2)

    content = input_path.read_text(encoding='utf-8')

    colors = extract_colors(content)
    fonts = extract_fonts(content)
    spacing = extract_spacing(content)

    total_tokens = len(colors) + len(fonts) + len(spacing)

    if args.format == 'pencil':
        result = {
            'status': 'found' if total_tokens > 0 else 'empty',
            'source': str(input_path),
            'variables': to_pencil_format(colors, fonts, spacing),
            'fonts': fonts,
            'summary': {
                'colors': len(colors),
                'fonts': len(fonts),
                'spacing': len(spacing),
                'total': total_tokens,
            },
        }
    else:
        result = {
            'status': 'found' if total_tokens > 0 else 'empty',
            'source': str(input_path),
            'colors': colors,
            'fonts': fonts,
            'spacing': spacing,
            'summary': {
                'colors': len(colors),
                'fonts': len(fonts),
                'spacing': len(spacing),
                'total': total_tokens,
            },
        }

    output = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f'Results written to {args.output}', file=sys.stderr)
    else:
        print(output)

    sys.exit(0 if total_tokens > 0 else 1)


if __name__ == '__main__':
    main()
