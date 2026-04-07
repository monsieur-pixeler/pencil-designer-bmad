#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Aggregate pattern counts from multiple subagent JSON reports.

Collects pattern arrays returned by parallel screen-analysis subagents,
groups by pattern type across all screens, counts total instances, and
identifies candidates for component extraction (>= threshold instances).

Used by [CH] Component Harvest to pre-aggregate subagent results before
the LLM reviews candidates — replacing 100-300 tokens of LLM aggregation
work with a deterministic script.

Usage:
    python3 aggregate-patterns.py --reports screen1.json screen2.json screen3.json
    python3 aggregate-patterns.py --reports-dir ./subagent-results/
    python3 aggregate-patterns.py --reports-dir ./results/ --threshold 3 --output candidates.json

Exit codes: 0=candidates found, 1=no candidates, 2=error
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path


def load_report(path: Path) -> dict:
    """Load a single subagent screen report."""
    data = json.loads(path.read_text(encoding='utf-8'))
    # Handle both direct reports and wrapped results
    if isinstance(data, list):
        return {'screen': path.stem, 'patterns': data}
    return data


def aggregate_reports(reports: list[dict]) -> dict[str, dict]:
    """Aggregate patterns across all reports, grouped by pattern type."""
    by_type: dict[str, dict] = defaultdict(lambda: {
        'type': '',
        'total_count': 0,
        'screens': [],
        'all_node_ids': [],
    })

    for report in reports:
        screen = report.get('screen', report.get('screen_name', 'unknown'))
        frame_id = report.get('frame_id', '')
        patterns = report.get('patterns', [])

        for pattern in patterns:
            ptype = pattern.get('type', pattern.get('pattern_type', 'unknown'))
            count = pattern.get('count', 1)
            node_ids = pattern.get('node_ids', pattern.get('nodes', []))

            agg = by_type[ptype]
            agg['type'] = ptype
            agg['total_count'] += count
            agg['all_node_ids'].extend(node_ids)
            agg['screens'].append({
                'screen': screen,
                'frame_id': frame_id,
                'count': count,
                'node_ids': node_ids,
            })

    return dict(by_type)


def identify_candidates(
    aggregated: dict[str, dict],
    threshold: int,
) -> tuple[list[dict], list[dict]]:
    """Split patterns into extraction candidates and below-threshold patterns."""
    candidates = []
    below_threshold = []

    for ptype, data in sorted(aggregated.items(), key=lambda x: -x[1]['total_count']):
        entry = {
            'type': ptype,
            'total_instances': data['total_count'],
            'screen_count': len(data['screens']),
            'screens': data['screens'],
            'sample_node_ids': data['all_node_ids'][:3],  # First 3 for reference
        }
        if data['total_count'] >= threshold:
            entry['extraction_priority'] = (
                'high' if data['total_count'] >= threshold * 2 else 'medium'
            )
            candidates.append(entry)
        else:
            below_threshold.append(entry)

    return candidates, below_threshold


def main():
    parser = argparse.ArgumentParser(
        description='Aggregate component pattern counts from parallel subagent screen reports'
    )

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--reports', nargs='+', metavar='FILE',
                             help='Individual report JSON files from subagents')
    input_group.add_argument('--reports-dir',
                             help='Directory containing all subagent report JSON files')

    parser.add_argument('--threshold', type=int, default=3,
                        help='Minimum instances to qualify as extraction candidate (default: 3)')
    parser.add_argument('--output',
                        help='Write JSON result to file instead of stdout')
    args = parser.parse_args()

    # Collect report files
    report_files: list[Path] = []
    if args.reports:
        report_files = [Path(r) for r in args.reports]
    elif args.reports_dir:
        reports_dir = Path(args.reports_dir)
        if not reports_dir.exists():
            print(json.dumps({'status': 'error', 'message': f'Directory not found: {reports_dir}'}))
            sys.exit(2)
        report_files = sorted(reports_dir.glob('*.json'))

    if not report_files:
        print(json.dumps({'status': 'error', 'message': 'No report files found'}))
        sys.exit(2)

    # Load all reports
    reports = []
    errors = []
    for path in report_files:
        try:
            reports.append(load_report(path))
        except (json.JSONDecodeError, OSError) as e:
            errors.append({'file': str(path), 'error': str(e)})

    if not reports:
        print(json.dumps({'status': 'error', 'message': 'All reports failed to load', 'errors': errors}))
        sys.exit(2)

    # Aggregate and classify
    aggregated = aggregate_reports(reports)
    candidates, below_threshold = identify_candidates(aggregated, args.threshold)

    result = {
        'status': 'candidates_found' if candidates else 'no_candidates',
        'screens_analyzed': len(reports),
        'pattern_types_found': len(aggregated),
        'threshold': args.threshold,
        'summary': {
            'extraction_candidates': len(candidates),
            'below_threshold': len(below_threshold),
            'total_instances': sum(d['total_count'] for d in aggregated.values()),
        },
        'candidates': candidates,
        'below_threshold': below_threshold,
    }
    if errors:
        result['load_errors'] = errors

    output = json.dumps(result, indent=2)
    if args.output:
        Path(args.output).write_text(output, encoding='utf-8')
        print(f'Results written to {args.output}', file=sys.stderr)
    else:
        print(output)

    sys.exit(0 if candidates else 1)


if __name__ == '__main__':
    main()
