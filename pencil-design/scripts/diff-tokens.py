#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Compare Pencil design token variables with code token files to detect drift.

Reads a JSON dump of Pencil variables (from get_variables MCP output) and
compares against code token files (SwiftUI ColorTokens.swift, globals.css,
tailwind.config.js, variables.css). Reports mismatches and missing tokens.

Usage:
    python3 diff-tokens.py --pencil variables.json --source {project-root}/src
    python3 diff-tokens.py --pencil variables.json --source {project-root}/RippedBodyCoach --framework swiftui
    python3 diff-tokens.py --pencil variables.json --source {project-root}/src --framework react --output drift.json

Exit codes: 0=no drift, 1=drift found, 2=error
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Regex patterns for extracting token values from code files
SWIFT_COLOR_RE = re.compile(
    r'(?:static\s+let|var|let)\s+(\w+)\s*[=:]\s*Color\((?:red:|hex:|#)?["\']?([#\w.,\s/]+)["\']?\)',
    re.IGNORECASE,
)
SWIFT_HEX_RE = re.compile(r'Color\(hex:\s*["\']([#0-9A-Fa-f]+)["\']')
CSS_VAR_RE = re.compile(r'--([\w-]+)\s*:\s*([^;]+);')
TAILWIND_COLOR_RE = re.compile(r'["\']?([\w-]+)["\']?\s*:\s*["\']([#\w]+)["\']')


def normalize_hex(value: str) -> str | None:
    """Normalize a hex color value to uppercase 6-char format."""
    value = value.strip().lstrip('#')
    m = re.match(r'^([0-9A-Fa-f]{3})$', value)
    if m:
        value = ''.join(c * 2 for c in value)
    if re.match(r'^[0-9A-Fa-f]{6}$', value):
        return '#' + value.upper()
    if re.match(r'^[0-9A-Fa-f]{8}$', value):  # with alpha — strip alpha for comparison
        return '#' + value[:6].upper()
    return None


def extract_swift_tokens(file_path: Path) -> dict[str, str]:
    """Extract color token name→hex from a Swift token file."""
    tokens = {}
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    for match in SWIFT_HEX_RE.finditer(content):
        hex_val = normalize_hex(match.group(1))
        if hex_val:
            # Try to find the variable name on the same line
            line_start = content.rfind('\n', 0, match.start()) + 1
            line = content[line_start:content.find('\n', match.end())]
            name_match = re.search(r'(?:let|var|static\s+let)\s+(\w+)', line)
            if name_match:
                tokens[name_match.group(1).lower()] = hex_val
    return tokens


def extract_css_tokens(file_path: Path) -> dict[str, str]:
    """Extract CSS custom property name→value."""
    tokens = {}
    content = file_path.read_text(encoding='utf-8', errors='ignore')
    for match in CSS_VAR_RE.finditer(content):
        name = match.group(1).strip()
        value = match.group(2).strip()
        hex_val = normalize_hex(value)
        if hex_val:
            tokens[name.lower()] = hex_val
    return tokens


def load_pencil_variables(variables_json: Path) -> dict[str, str]:
    """Load Pencil variables from MCP get_variables JSON output."""
    data = json.loads(variables_json.read_text(encoding='utf-8'))
    tokens = {}

    # Handle both raw MCP output formats
    items = data if isinstance(data, list) else data.get('variables', data.get('items', []))
    for item in items:
        name = item.get('name', '').lower().replace(' ', '-').replace('/', '-')
        value = item.get('value', item.get('resolvedValue', ''))
        if isinstance(value, str):
            hex_val = normalize_hex(value)
            if hex_val:
                tokens[name] = hex_val
        elif isinstance(value, dict):
            # RGBA dict: {r: 0-1, g: 0-1, b: 0-1, a: 0-1}
            r = value.get('r', 0)
            g = value.get('g', 0)
            b = value.get('b', 0)
            hex_val = '#{:02X}{:02X}{:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            )
            tokens[name] = hex_val

    return tokens


def find_code_token_files(source_dir: Path, framework: str) -> list[Path]:
    """Discover token files based on framework."""
    patterns = {
        'swiftui': ['**/DesignSystem/ColorTokens.swift', '**/DesignSystem/Colors.swift',
                    '**/Typography.swift', '**/DesignSystem/*.swift'],
        'react':   ['**/globals.css', '**/variables.css', '**/tailwind.config.js',
                    '**/tailwind.config.ts', '**/tokens.css'],
        'css':     ['**/variables.css', '**/tokens.css', '**/design-tokens.css'],
    }
    found = []
    skip = {'node_modules', '.git', 'dist', 'build', 'DerivedData', '.build'}
    for pattern in patterns.get(framework, patterns['react'] + patterns['swiftui']):
        for p in source_dir.rglob(pattern.lstrip('*/')):
            if not any(s in p.parts for s in skip):
                found.append(p)
    return list(dict.fromkeys(found))  # deduplicate preserving order


def diff_tokens(pencil: dict[str, str], code: dict[str, str]) -> dict:
    """Compare pencil tokens against code tokens, return drift report."""
    drifted = []
    missing_in_code = []
    missing_in_pencil = []

    for name, pencil_hex in pencil.items():
        if name in code:
            if code[name] != pencil_hex:
                drifted.append({
                    'token': name,
                    'pencil': pencil_hex,
                    'code': code[name],
                    'severity': 'high',
                })
        else:
            # Try matching by value (name might differ)
            code_values = {v: k for k, v in code.items()}
            if pencil_hex in code_values:
                # Same value, different name — note but not a critical drift
                drifted.append({
                    'token': name,
                    'pencil': pencil_hex,
                    'code_name': code_values[pencil_hex],
                    'note': 'same value, different token name',
                    'severity': 'medium',
                })
            else:
                missing_in_code.append({
                    'token': name,
                    'pencil': pencil_hex,
                    'severity': 'medium',
                })

    for name, code_hex in code.items():
        if name not in pencil:
            missing_in_pencil.append({
                'token': name,
                'code': code_hex,
                'severity': 'low',
            })

    total_checks = len(pencil) + len(missing_in_pencil)
    drift_count = len(drifted) + len(missing_in_code)
    sync_pct = round((1 - drift_count / max(total_checks, 1)) * 100)

    return {
        'status': 'clean' if drift_count == 0 else 'drift',
        'sync_percent': sync_pct,
        'pencil_token_count': len(pencil),
        'code_token_count': len(code),
        'drifted': drifted,
        'missing_in_code': missing_in_code,
        'missing_in_pencil': missing_in_pencil,
        'summary': {
            'drifted': len(drifted),
            'missing_in_code': len(missing_in_code),
            'missing_in_pencil': len(missing_in_pencil),
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description='Compare Pencil design tokens with code tokens to detect drift'
    )
    parser.add_argument('--pencil', required=True,
                        help='Path to get_variables JSON output from Pencil MCP')
    parser.add_argument('--source', required=True,
                        help='Project source directory to scan for code token files')
    parser.add_argument('--framework',
                        choices=['swiftui', 'react', 'css', 'auto'],
                        default='auto',
                        help='Code framework (default: auto-detect)')
    parser.add_argument('--output',
                        help='Write JSON result to file instead of stdout')
    args = parser.parse_args()

    pencil_path = Path(args.pencil)
    source_dir = Path(args.source)

    if not pencil_path.exists():
        print(json.dumps({'status': 'error', 'message': f'Pencil variables file not found: {pencil_path}'}))
        sys.exit(2)
    if not source_dir.exists():
        print(json.dumps({'status': 'error', 'message': f'Source directory not found: {source_dir}'}))
        sys.exit(2)

    # Load Pencil tokens
    pencil_tokens = load_pencil_variables(pencil_path)
    if not pencil_tokens:
        print(json.dumps({'status': 'warning', 'message': 'No color tokens found in Pencil variables file'}))
        sys.exit(0)

    # Discover and parse code token files
    framework = args.framework
    token_files = find_code_token_files(source_dir, framework)

    code_tokens: dict[str, str] = {}
    files_read = []
    for f in token_files:
        try:
            if f.suffix == '.swift':
                code_tokens.update(extract_swift_tokens(f))
            else:
                code_tokens.update(extract_css_tokens(f))
            files_read.append(str(f))
        except Exception as e:
            pass  # Skip unreadable files

    result = diff_tokens(pencil_tokens, code_tokens)
    result['files_read'] = files_read
    result['source_dir'] = str(source_dir)

    output = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f'Results written to {args.output}', file=sys.stderr)
    else:
        print(output)

    sys.exit(0 if result['status'] == 'clean' else 1)


if __name__ == '__main__':
    main()
