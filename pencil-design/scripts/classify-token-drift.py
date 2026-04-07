#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Classify unique property values from Pencil frames against known design tokens.

Takes search_all_unique_properties JSON output (from Pencil MCP) and a set of
known token values (from get_variables or DESIGN.md), then classifies each unique
value as: tokenized, near-match (drift), or hardcoded.

Used by [AA] App Audit and [ID] Import Design to pre-classify values before
the LLM analyzes them — replacing 150-300 tokens of LLM comparison work with
a deterministic script.

Usage:
    python3 classify-token-drift.py --properties unique-props.json --tokens variables.json
    python3 classify-token-drift.py --properties unique-props.json --tokens variables.json --output classified.json
    python3 classify-token-drift.py --properties unique-props.json --tokens variables.json --tolerance 2

Exit codes: 0=all tokenized, 1=drift found, 2=error
"""

import argparse
import json
import math
import sys
from pathlib import Path


def hex_to_rgb(hex_val: str) -> tuple[int, int, int] | None:
    """Convert hex color to (r, g, b) tuple."""
    hex_val = hex_val.strip().lstrip('#')
    if len(hex_val) == 3:
        hex_val = ''.join(c * 2 for c in hex_val)
    if len(hex_val) not in (6, 8):
        return None
    try:
        return (int(hex_val[0:2], 16), int(hex_val[2:4], 16), int(hex_val[4:6], 16))
    except ValueError:
        return None


def color_distance(hex_a: str, hex_b: str) -> float:
    """Euclidean distance in RGB space between two hex colors."""
    rgb_a = hex_to_rgb(hex_a)
    rgb_b = hex_to_rgb(hex_b)
    if not rgb_a or not rgb_b:
        return float('inf')
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb_a, rgb_b)))


def normalize_hex(value: str) -> str | None:
    """Normalize hex color to uppercase 6-char."""
    value = value.strip().lstrip('#')
    if len(value) == 3:
        value = ''.join(c * 2 for c in value)
    if len(value) in (6, 8):
        return '#' + value[:6].upper()
    return None


def load_token_values(variables_json: Path) -> dict[str, str]:
    """Load token name→hex from Pencil get_variables JSON."""
    data = json.loads(variables_json.read_text(encoding='utf-8'))
    tokens = {}
    items = data if isinstance(data, list) else data.get('variables', data.get('items', []))
    for item in items:
        name = item.get('name', '').strip()
        value = item.get('value', item.get('resolvedValue', ''))
        if isinstance(value, str):
            hex_val = normalize_hex(value)
            if hex_val:
                tokens[name] = hex_val
        elif isinstance(value, dict):
            r, g, b = value.get('r', 0), value.get('g', 0), value.get('b', 0)
            tokens[name] = '#{:02X}{:02X}{:02X}'.format(
                int(r * 255), int(g * 255), int(b * 255)
            )
    return tokens


def load_unique_properties(props_json: Path) -> dict[str, list]:
    """Load search_all_unique_properties JSON output."""
    data = json.loads(props_json.read_text(encoding='utf-8'))
    # Handle both raw list and MCP wrapper
    if isinstance(data, list):
        return {'values': data}
    return data


def classify_value(
    value: str,
    tokens: dict[str, str],
    near_tolerance: float,
) -> dict:
    """Classify a single value against known tokens."""
    hex_val = normalize_hex(value)

    if not hex_val:
        # Non-color value (spacing, font size, etc.)
        return {
            'value': value,
            'classification': 'non-color',
            'note': 'Numeric or named value — manual review needed',
        }

    # Exact match
    for token_name, token_hex in tokens.items():
        if token_hex == hex_val:
            return {
                'value': value,
                'hex': hex_val,
                'classification': 'tokenized',
                'token': token_name,
                'token_value': token_hex,
            }

    # Near-match (drift)
    best_match = None
    best_distance = float('inf')
    for token_name, token_hex in tokens.items():
        dist = color_distance(hex_val, token_hex)
        if dist < best_distance:
            best_distance = dist
            best_match = (token_name, token_hex)

    if best_match and best_distance <= near_tolerance:
        return {
            'value': value,
            'hex': hex_val,
            'classification': 'near-match',
            'severity': 'high',
            'nearest_token': best_match[0],
            'nearest_value': best_match[1],
            'distance': round(best_distance, 1),
            'fix': f'Replace {hex_val} with {best_match[1]} (token: {best_match[0]})',
        }

    # Hardcoded — no match
    return {
        'value': value,
        'hex': hex_val,
        'classification': 'hardcoded',
        'severity': 'medium',
        'note': 'No matching token — consider adding to design system',
    }


def main():
    parser = argparse.ArgumentParser(
        description='Classify unique Pencil property values against design tokens'
    )
    parser.add_argument('--properties', required=True,
                        help='JSON from search_all_unique_properties MCP tool')
    parser.add_argument('--tokens', required=True,
                        help='JSON from get_variables MCP tool')
    parser.add_argument('--output',
                        help='Write JSON result to file instead of stdout')
    parser.add_argument('--tolerance', type=float, default=8.0,
                        help='Max RGB distance to consider a near-match (default: 8)')
    args = parser.parse_args()

    props_path = Path(args.properties)
    tokens_path = Path(args.tokens)

    for p in (props_path, tokens_path):
        if not p.exists():
            print(json.dumps({'status': 'error', 'message': f'File not found: {p}'}))
            sys.exit(2)

    tokens = load_token_values(tokens_path)
    props_data = load_unique_properties(props_path)

    # Extract values to classify — handle multiple input formats
    values_to_check: list[str] = []
    if 'values' in props_data:
        raw = props_data['values']
        if raw and isinstance(raw[0], dict):
            values_to_check = [v.get('value', '') for v in raw]
        else:
            values_to_check = [str(v) for v in raw]
    elif isinstance(props_data, dict):
        for prop_values in props_data.values():
            if isinstance(prop_values, list):
                values_to_check.extend(str(v) for v in prop_values)

    classifications = [classify_value(v, tokens, args.tolerance) for v in values_to_check if v]

    by_class = {
        'tokenized': [c for c in classifications if c['classification'] == 'tokenized'],
        'near_match': [c for c in classifications if c['classification'] == 'near-match'],
        'hardcoded': [c for c in classifications if c['classification'] == 'hardcoded'],
        'non_color': [c for c in classifications if c['classification'] == 'non-color'],
    }

    drift_count = len(by_class['near_match']) + len(by_class['hardcoded'])

    result = {
        'status': 'clean' if drift_count == 0 else 'drift',
        'token_count': len(tokens),
        'values_checked': len(classifications),
        'summary': {
            'tokenized': len(by_class['tokenized']),
            'near_match': len(by_class['near_match']),
            'hardcoded': len(by_class['hardcoded']),
            'non_color': len(by_class['non_color']),
        },
        'near_matches': by_class['near_match'],
        'hardcoded': by_class['hardcoded'],
        'tokenized': by_class['tokenized'],
    }

    output = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f'Results written to {args.output}', file=sys.stderr)
    else:
        print(output)

    sys.exit(0 if result['status'] == 'clean' else 1)


if __name__ == '__main__':
    main()
