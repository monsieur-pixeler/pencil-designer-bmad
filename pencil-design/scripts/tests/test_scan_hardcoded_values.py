#!/usr/bin/env python3
"""Unit tests for scan-hardcoded-values.py"""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent


def load_module(name: str):
    path = SCRIPTS_DIR / f'{name}.py'
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mod = load_module('scan-hardcoded-values')
scan_file = mod.scan_file
DEFAULT_TOKENS = mod.DEFAULT_TOKENS


class TestScanFile(unittest.TestCase):
    def write_temp(self, content: str, suffix: str = '.swift') -> Path:
        f = tempfile.NamedTemporaryFile(
            mode='w', suffix=suffix, delete=False, encoding='utf-8'
        )
        f.write(content)
        f.close()
        return Path(f.name)

    def test_detects_known_surface_color(self):
        path = self.write_temp('let bg = "#F4F4F5"\n')
        findings = scan_file(path, DEFAULT_TOKENS)
        colors = [f for f in findings if f['type'] == 'hardcoded_color']
        self.assertTrue(any(f['value'] == '#F4F4F5' for f in colors))

    def test_skips_comment_lines_swift(self):
        path = self.write_temp('// Color: #F4F4F5 — surface\n')
        findings = scan_file(path, DEFAULT_TOKENS)
        self.assertEqual(len(findings), 0)

    def test_detects_inter_font(self):
        path = self.write_temp('.font(.custom("Inter", size: 14))\n')
        findings = scan_file(path, DEFAULT_TOKENS)
        fonts = [f for f in findings if f['type'] == 'hardcoded_font']
        self.assertGreater(len(fonts), 0)

    def test_detects_outfit_font(self):
        path = self.write_temp('Font.custom("Outfit", size: 24)\n')
        findings = scan_file(path, DEFAULT_TOKENS)
        fonts = [f for f in findings if f['type'] == 'hardcoded_font']
        self.assertGreater(len(fonts), 0)

    def test_unknown_color_not_flagged(self):
        path = self.write_temp('Color(hex: "#ABCDEF")\n')
        findings = scan_file(path, DEFAULT_TOKENS)
        colors = [f for f in findings if f['type'] == 'hardcoded_color']
        self.assertEqual(len(colors), 0)

    def test_css_file(self):
        path = self.write_temp(
            ':root { color: #FFFFFF; background: #F4F4F5; }\n',
            suffix='.css'
        )
        findings = scan_file(path, DEFAULT_TOKENS)
        colors = [f for f in findings if f['type'] == 'hardcoded_color']
        self.assertGreaterEqual(len(colors), 1)

    def test_tsx_file(self):
        path = self.write_temp(
            'const style = { color: "#000000", background: "#F4F4F5" };\n',
            suffix='.tsx'
        )
        findings = scan_file(path, DEFAULT_TOKENS)
        colors = [f for f in findings if f['type'] == 'hardcoded_color']
        self.assertGreaterEqual(len(colors), 1)

    def test_returns_line_numbers(self):
        path = self.write_temp(
            'let x = 1\nlet color = "#F4F4F5"\nlet y = 2\n'
        )
        findings = scan_file(path, DEFAULT_TOKENS)
        colors = [f for f in findings if f['type'] == 'hardcoded_color']
        self.assertTrue(any(f['line'] == 2 for f in colors))

    def test_severity_set(self):
        path = self.write_temp('color: "#000000"\n')
        findings = scan_file(path, DEFAULT_TOKENS)
        for f in findings:
            self.assertIn('severity', f)
            self.assertIn(f['severity'], ('high', 'medium', 'low'))


if __name__ == '__main__':
    unittest.main()
