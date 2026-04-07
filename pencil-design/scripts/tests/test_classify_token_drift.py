#!/usr/bin/env python3
"""Unit tests for classify-token-drift.py and aggregate-patterns.py"""

import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent


def load_module(name: str):
    path = SCRIPTS_DIR / f'{name}.py'
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ct_mod = load_module('classify-token-drift')
normalize_hex = ct_mod.normalize_hex
hex_to_rgb = ct_mod.hex_to_rgb
color_distance = ct_mod.color_distance
classify_value = ct_mod.classify_value

ap_mod = load_module('aggregate-patterns')
aggregate_reports = ap_mod.aggregate_reports
identify_candidates = ap_mod.identify_candidates


class TestNormalizeHex(unittest.TestCase):
    def test_six_char(self):
        self.assertEqual(normalize_hex('#F4F4F5'), '#F4F4F5')

    def test_three_char_expands(self):
        self.assertEqual(normalize_hex('#FFF'), '#FFFFFF')

    def test_eight_char_strips_alpha(self):
        self.assertEqual(normalize_hex('#F4F4F5FF'), '#F4F4F5')

    def test_invalid_returns_none(self):
        self.assertIsNone(normalize_hex('not-a-color'))

    def test_no_hash(self):
        self.assertEqual(normalize_hex('F4F4F5'), '#F4F4F5')


class TestHexToRgb(unittest.TestCase):
    def test_black(self):
        self.assertEqual(hex_to_rgb('#000000'), (0, 0, 0))

    def test_white(self):
        self.assertEqual(hex_to_rgb('#FFFFFF'), (255, 255, 255))

    def test_mixed(self):
        self.assertEqual(hex_to_rgb('#F4F4F5'), (244, 244, 245))

    def test_invalid(self):
        self.assertIsNone(hex_to_rgb('gg0000'))


class TestColorDistance(unittest.TestCase):
    def test_identical(self):
        self.assertAlmostEqual(color_distance('#F4F4F5', '#F4F4F5'), 0.0)

    def test_slightly_different(self):
        # #F4F4F5 vs #F5F5F5: all channels off by 1 → sqrt(3) ≈ 1.73
        dist = color_distance('#F4F4F5', '#F5F5F5')
        self.assertLess(dist, 5.0)
        self.assertGreater(dist, 0.0)

    def test_very_different(self):
        dist = color_distance('#000000', '#FFFFFF')
        self.assertGreater(dist, 400)

    def test_invalid_returns_inf(self):
        self.assertEqual(color_distance('invalid', '#FFFFFF'), float('inf'))


class TestClassifyValue(unittest.TestCase):
    TOKENS = {
        'color/surface': '#F4F4F5',
        'color/bg': '#FFFFFF',
        'color/text-primary': '#000000',
    }

    def test_exact_match(self):
        result = classify_value('#F4F4F5', self.TOKENS, near_tolerance=8.0)
        self.assertEqual(result['classification'], 'tokenized')
        self.assertEqual(result['token'], 'color/surface')

    def test_near_match_within_tolerance(self):
        # #F5F5F5 is close to #F4F4F5 (distance ~1.73)
        result = classify_value('#F5F5F5', self.TOKENS, near_tolerance=8.0)
        self.assertEqual(result['classification'], 'near-match')
        self.assertIn('nearest_token', result)

    def test_hardcoded_no_match(self):
        result = classify_value('#AABBCC', self.TOKENS, near_tolerance=8.0)
        self.assertEqual(result['classification'], 'hardcoded')

    def test_non_color_value(self):
        result = classify_value('16', self.TOKENS, near_tolerance=8.0)
        self.assertEqual(result['classification'], 'non-color')

    def test_lowercase_hex_matches(self):
        result = classify_value('#f4f4f5', self.TOKENS, near_tolerance=8.0)
        self.assertEqual(result['classification'], 'tokenized')

    def test_near_match_outside_tolerance(self):
        # Very different color with tight tolerance
        result = classify_value('#AABBCC', self.TOKENS, near_tolerance=2.0)
        self.assertEqual(result['classification'], 'hardcoded')


class TestAggregateReports(unittest.TestCase):
    def test_basic_aggregation(self):
        reports = [
            {
                'screen': 'Dashboard',
                'patterns': [
                    {'type': 'section_header', 'count': 3, 'node_ids': ['a', 'b', 'c']},
                    {'type': 'metric_row', 'count': 2, 'node_ids': ['d', 'e']},
                ],
            },
            {
                'screen': 'Settings',
                'patterns': [
                    {'type': 'section_header', 'count': 2, 'node_ids': ['f', 'g']},
                ],
            },
        ]
        result = aggregate_reports(reports)
        self.assertIn('section_header', result)
        self.assertEqual(result['section_header']['total_count'], 5)
        self.assertEqual(result['metric_row']['total_count'], 2)
        self.assertEqual(len(result['section_header']['screens']), 2)

    def test_empty_patterns(self):
        reports = [{'screen': 'Empty', 'patterns': []}]
        result = aggregate_reports(reports)
        self.assertEqual(len(result), 0)

    def test_single_screen(self):
        reports = [{'screen': 'A', 'patterns': [
            {'type': 'card', 'count': 4, 'node_ids': ['x1', 'x2', 'x3', 'x4']},
        ]}]
        result = aggregate_reports(reports)
        self.assertEqual(result['card']['total_count'], 4)


class TestIdentifyCandidates(unittest.TestCase):
    def make_aggregated(self, patterns: dict[str, int]) -> dict:
        return {
            ptype: {'type': ptype, 'total_count': count, 'screens': [], 'all_node_ids': []}
            for ptype, count in patterns.items()
        }

    def test_threshold_filtering(self):
        aggregated = self.make_aggregated({'header': 5, 'button': 2, 'card': 8})
        candidates, below = identify_candidates(aggregated, threshold=3)
        candidate_types = {c['type'] for c in candidates}
        below_types = {b['type'] for b in below}
        self.assertIn('header', candidate_types)
        self.assertIn('card', candidate_types)
        self.assertIn('button', below_types)

    def test_high_priority_marking(self):
        aggregated = self.make_aggregated({'section': 10})
        candidates, _ = identify_candidates(aggregated, threshold=3)
        self.assertEqual(candidates[0]['extraction_priority'], 'high')

    def test_medium_priority(self):
        aggregated = self.make_aggregated({'section': 4})
        candidates, _ = identify_candidates(aggregated, threshold=3)
        self.assertEqual(candidates[0]['extraction_priority'], 'medium')

    def test_all_below_threshold(self):
        aggregated = self.make_aggregated({'tiny': 1, 'small': 2})
        candidates, below = identify_candidates(aggregated, threshold=3)
        self.assertEqual(len(candidates), 0)
        self.assertEqual(len(below), 2)


if __name__ == '__main__':
    unittest.main()
