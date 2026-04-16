#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Validate interactive element touch targets meet minimum size requirements.

Reads a JSON dump of batch_get output (with node widths/heights) and validates
that interactive elements (buttons, links, inputs, toggles) are at least 44x44px.
Reports pass/fail per element.

Usage:
    python3 touch-target-validator.py --input nodes.json
    python3 touch-target-validator.py --input nodes.json --min-size 48
    python3 touch-target-validator.py --input nodes.json --output report.json
    python3 touch-target-validator.py --input nodes.json --platform ios

Exit codes: 0=all pass, 1=failures found, 2=error
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Interactive element detection patterns (name or type-based)
INTERACTIVE_PATTERNS = re.compile(
    r'(?i)(button|btn|cta|toggle|switch|checkbox|radio|input|textfield|'
    r'link|tab|stepper|slider|picker|select|menu-item|nav-item|icon-button|'
    r'close|dismiss|back|forward|add|remove|delete|edit|save|cancel|submit)',
)

# Platform-specific minimum sizes (in points/pixels)
PLATFORM_SIZES = {
    'ios': 44,
    'android': 48,
    'web': 44,  # WCAG 2.5.8 Target Size (Minimum)
    'macos': 24,  # macOS uses pointer — smaller targets acceptable
}


def flatten_tree(node: dict, path: str = '') -> list[dict]:
    """Flatten a node tree into a list of nodes with path metadata."""
    name = node.get('name', node.get('id', 'unnamed'))
    current_path = f'{path}/{name}' if path else name
    node_with_path = {**node, '_path': current_path}
    result = [node_with_path]
    for child in node.get('children', []):
        result.extend(flatten_tree(child, current_path))
    return result


def is_interactive(node: dict) -> bool:
    """Detect if a node is likely an interactive element."""
    name = node.get('name', '')
    node_type = node.get('type', '')

    # Check name patterns
    if INTERACTIVE_PATTERNS.search(name):
        return True

    # Check type patterns
    if node_type.lower() in ('button', 'input', 'link', 'toggle', 'switch'):
        return True

    # Check for click/tap handlers in metadata
    if node.get('onClick') or node.get('onTap') or node.get('action'):
        return True

    return False


def validate_node(node: dict, min_size: float) -> dict:
    """Validate a single interactive node's touch target size."""
    width = node.get('width', 0)
    height = node.get('height', 0)
    name = node.get('name', node.get('id', 'unnamed'))

    width_pass = width >= min_size
    height_pass = height >= min_size

    return {
        'name': name,
        'path': node.get('_path', name),
        'width': width,
        'height': height,
        'min_required': min_size,
        'width_pass': width_pass,
        'height_pass': height_pass,
        'pass': width_pass and height_pass,
        'issue': None if (width_pass and height_pass) else
            f'{width}x{height}px — minimum {min_size}x{min_size}px required',
    }


def load_nodes(path: Path) -> list[dict]:
    """Load nodes from JSON file. Handles raw node, list, or MCP batch_get wrapper."""
    data = json.loads(path.read_text(encoding='utf-8'))

    if isinstance(data, dict):
        if 'nodes' in data:
            nodes = data['nodes']
            return nodes if isinstance(nodes, list) else [nodes]
        if 'result' in data:
            result = data['result']
            return result if isinstance(result, list) else [result]
        return [data]
    if isinstance(data, list):
        return data
    return []


def main():
    parser = argparse.ArgumentParser(
        description='Validate interactive element touch targets meet minimum size'
    )
    parser.add_argument('--input', required=True,
                        help='JSON file with node tree (batch_get output)')
    parser.add_argument('--min-size', type=float, default=None,
                        help='Minimum touch target size in px (default: 44, or platform-specific)')
    parser.add_argument('--platform', choices=list(PLATFORM_SIZES.keys()),
                        default='ios',
                        help='Target platform for size requirements (default: ios)')
    parser.add_argument('--output',
                        help='Write JSON result to file instead of stdout')
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(json.dumps({'status': 'error', 'message': f'File not found: {input_path}'}))
        sys.exit(2)

    min_size = args.min_size or PLATFORM_SIZES.get(args.platform, 44)

    try:
        root_nodes = load_nodes(input_path)
    except (json.JSONDecodeError, KeyError) as e:
        print(json.dumps({'status': 'error', 'message': f'Failed to parse JSON: {e}'}))
        sys.exit(2)

    # Flatten all trees and find interactive elements
    all_nodes = []
    for root in root_nodes:
        all_nodes.extend(flatten_tree(root))

    interactive = [n for n in all_nodes if is_interactive(n)]

    # Validate each interactive element
    results = [validate_node(n, min_size) for n in interactive]
    failures = [r for r in results if not r['pass']]
    passes = [r for r in results if r['pass']]

    report = {
        'status': 'pass' if not failures else 'fail',
        'platform': args.platform,
        'min_size': min_size,
        'summary': {
            'interactive_elements': len(results),
            'passed': len(passes),
            'failed': len(failures),
        },
        'failures': failures,
        'passes': passes,
    }

    output = json.dumps(report, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f'Results written to {args.output}', file=sys.stderr)
    else:
        print(output)

    sys.exit(0 if not failures else 1)


if __name__ == '__main__':
    main()
