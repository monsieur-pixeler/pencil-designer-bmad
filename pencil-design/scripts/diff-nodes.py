#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Diff two Pencil node trees depth-first to produce a structured change list.

Reads two JSON node trees (from batch_get MCP output) and compares them,
matching nodes by name then by id. Reports additions, removals, and property
changes (fill, fontSize, fontWeight, fontFamily, gap, padding, width, height,
cornerRadius, content, opacity, visible).

Usage:
    python3 diff-nodes.py --before frame-a.json --after frame-b.json
    python3 diff-nodes.py --before frame-a.json --after frame-b.json --output diff.json
    python3 diff-nodes.py --before frame-a.json --after frame-b.json --ignore-position

Exit codes: 0=no changes, 1=changes found, 2=error
"""

import argparse
import json
import sys
from pathlib import Path

# Properties to compare when diffing nodes
TRACKED_PROPERTIES = {
    'fill',
    'fills',
    'stroke',
    'fontSize',
    'fontWeight',
    'fontFamily',
    'letterSpacing',
    'lineHeight',
    'gap',
    'padding',
    'paddingTop',
    'paddingBottom',
    'paddingLeft',
    'paddingRight',
    'width',
    'height',
    'cornerRadius',
    'content',
    'opacity',
    'visible',
    'reusable',
    'layout',
    'alignItems',
    'justifyContent',
}

POSITION_PROPERTIES = {'x', 'y'}


def flatten_tree(node: dict, path: str = '') -> dict[str, dict]:
    """Flatten a node tree into a path→node dict using name-based paths."""
    name = node.get('name', node.get('id', 'unnamed'))
    current_path = f'{path}/{name}' if path else name
    result = {current_path: node}
    for child in node.get('children', []):
        result.update(flatten_tree(child, current_path))
    return result


def compare_value(a, b) -> bool:
    """Return True if values are considered equal (with tolerance for floats)."""
    if type(a) != type(b):
        return False
    if isinstance(a, float) and isinstance(b, float):
        return abs(a - b) < 0.5  # sub-pixel tolerance
    if isinstance(a, dict) and isinstance(b, dict):
        return all(compare_value(a.get(k), b.get(k)) for k in set(a) | set(b))
    return a == b


def diff_node_properties(before: dict, after: dict, include_position: bool) -> list[dict]:
    """Return list of property changes between two nodes."""
    changes = []
    props = TRACKED_PROPERTIES | (POSITION_PROPERTIES if include_position else set())

    for prop in props:
        before_val = before.get(prop)
        after_val = after.get(prop)
        if before_val is None and after_val is None:
            continue
        if not compare_value(before_val, after_val):
            changes.append({
                'property': prop,
                'before': before_val,
                'after': after_val,
            })

    return changes


def diff_trees(before_root: dict, after_root: dict, include_position: bool) -> dict:
    """Diff two node trees, returning a structured change report."""
    before_flat = flatten_tree(before_root)
    after_flat = flatten_tree(after_root)

    added = []
    removed = []
    changed = []

    before_paths = set(before_flat.keys())
    after_paths = set(after_flat.keys())

    # Added nodes
    for path in after_paths - before_paths:
        node = after_flat[path]
        added.append({
            'path': path,
            'type': node.get('type', 'unknown'),
            'name': node.get('name', ''),
        })

    # Removed nodes
    for path in before_paths - after_paths:
        node = before_flat[path]
        removed.append({
            'path': path,
            'type': node.get('type', 'unknown'),
            'name': node.get('name', ''),
        })

    # Changed nodes
    for path in before_paths & after_paths:
        before_node = before_flat[path]
        after_node = after_flat[path]
        prop_changes = diff_node_properties(before_node, after_node, include_position)
        if prop_changes:
            changed.append({
                'path': path,
                'name': before_node.get('name', ''),
                'type': before_node.get('type', 'unknown'),
                'changes': prop_changes,
            })

    total_changes = len(added) + len(removed) + len(changed)

    return {
        'status': 'no_changes' if total_changes == 0 else 'changed',
        'summary': {
            'added': len(added),
            'removed': len(removed),
            'changed': len(changed),
            'total': total_changes,
        },
        'added': added,
        'removed': removed,
        'changed': changed,
    }


def load_node_tree(path: Path) -> dict:
    """Load a node tree from a JSON file. Handles both raw node and MCP batch_get wrapper."""
    data = json.loads(path.read_text(encoding='utf-8'))

    # Handle MCP batch_get response wrapper
    if isinstance(data, dict):
        if 'nodes' in data:
            nodes = data['nodes']
            return nodes[0] if isinstance(nodes, list) and nodes else data
        if 'result' in data:
            result = data['result']
            if isinstance(result, list):
                return result[0] if result else data
    if isinstance(data, list):
        return data[0] if data else {}

    return data


def main():
    parser = argparse.ArgumentParser(
        description='Diff two Pencil node trees to show exactly what changed'
    )
    parser.add_argument('--before', required=True,
                        help='JSON file with the before frame (batch_get output)')
    parser.add_argument('--after', required=True,
                        help='JSON file with the after frame (batch_get output)')
    parser.add_argument('--output',
                        help='Write JSON result to file instead of stdout')
    parser.add_argument('--ignore-position', action='store_true',
                        help='Ignore x/y position changes (focus on structure and style)')
    args = parser.parse_args()

    before_path = Path(args.before)
    after_path = Path(args.after)

    for p in (before_path, after_path):
        if not p.exists():
            print(json.dumps({'status': 'error', 'message': f'File not found: {p}'}))
            sys.exit(2)

    try:
        before_tree = load_node_tree(before_path)
        after_tree = load_node_tree(after_path)
    except (json.JSONDecodeError, KeyError) as e:
        print(json.dumps({'status': 'error', 'message': f'Failed to parse JSON: {e}'}))
        sys.exit(2)

    include_position = not args.ignore_position
    result = diff_trees(before_tree, after_tree, include_position)
    result['before_file'] = str(before_path)
    result['after_file'] = str(after_path)

    output = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f'Results written to {args.output}', file=sys.stderr)
    else:
        print(output)

    sys.exit(0 if result['status'] == 'no_changes' else 1)


if __name__ == '__main__':
    main()
