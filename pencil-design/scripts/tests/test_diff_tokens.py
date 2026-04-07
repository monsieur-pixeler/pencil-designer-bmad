#!/usr/bin/env python3
"""Unit tests for diff-tokens.py"""

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent


def load_module(name: str):
    """Load a script module that has hyphens in its filename."""
    path = SCRIPTS_DIR / f'{name}.py'
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


mod = load_module('diff-tokens')
normalize_hex = mod.normalize_hex
diff_tokens = mod.diff_tokens
load_pencil_variables = mod.load_pencil_variables


class TestNormalizeHex(unittest.TestCase):
    def test_six_char(self):
        self.assertEqual(normalize_hex('#F4F4F5'), '#F4F4F5')

    def test_lowercase(self):
        self.assertEqual(normalize_hex('#f4f4f5'), '#F4F4F5')

    def test_three_char(self):
        self.assertEqual(normalize_hex('#FFF'), '#FFFFFF')

    def test_no_hash(self):
        self.assertEqual(normalize_hex('000000'), '#000000')

    def test_eight_char_strips_alpha(self):
        self.assertEqual(normalize_hex('#F4F4F5FF'), '#F4F4F5')

    def test_invalid(self):
        self.assertIsNone(normalize_hex('not-a-color'))

    def test_empty(self):
        self.assertIsNone(normalize_hex(''))


class TestDiffTokens(unittest.TestCase):
    def test_clean_match(self):
        pencil = {'surface': '#F4F4F5', 'text-primary': '#000000'}
        code = {'surface': '#F4F4F5', 'text-primary': '#000000'}
        result = diff_tokens(pencil, code)
        self.assertEqual(result['status'], 'clean')
        self.assertEqual(result['summary']['drifted'], 0)

    def test_drifted_value(self):
        pencil = {'surface': '#F4F4F5'}
        code = {'surface': '#F5F5F5'}
        result = diff_tokens(pencil, code)
        self.assertEqual(result['status'], 'drift')
        self.assertEqual(len(result['drifted']), 1)
        self.assertEqual(result['drifted'][0]['token'], 'surface')

    def test_missing_in_code(self):
        pencil = {'surface': '#F4F4F5', 'new-token': '#AAAAAA'}
        code = {'surface': '#F4F4F5'}
        result = diff_tokens(pencil, code)
        self.assertEqual(result['status'], 'drift')
        self.assertEqual(len(result['missing_in_code']), 1)

    def test_missing_in_pencil(self):
        pencil = {'surface': '#F4F4F5'}
        code = {'surface': '#F4F4F5', 'legacy-color': '#BBBBBB'}
        result = diff_tokens(pencil, code)
        self.assertEqual(len(result['missing_in_pencil']), 1)

    def test_empty_inputs(self):
        result = diff_tokens({}, {})
        self.assertEqual(result['status'], 'clean')


class TestLoadPencilVariables(unittest.TestCase):
    def test_list_format(self):
        variables = [
            {'name': 'color/surface', 'value': '#F4F4F5'},
            {'name': 'color/bg', 'value': '#FFFFFF'},
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(variables, f)
            path = Path(f.name)
        try:
            tokens = load_pencil_variables(path)
            self.assertIn('color-surface', tokens)
            self.assertEqual(tokens['color-surface'], '#F4F4F5')
        finally:
            path.unlink()

    def test_rgba_dict_format(self):
        variables = [
            {'name': 'accent', 'value': {'r': 1.0, 'g': 0.5, 'b': 0.0, 'a': 1.0}},
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(variables, f)
            path = Path(f.name)
        try:
            tokens = load_pencil_variables(path)
            self.assertIn('accent', tokens)
            self.assertEqual(tokens['accent'], '#FF7F00')
        finally:
            path.unlink()

    def test_wrapped_format(self):
        data = {'variables': [{'name': 'bg', 'value': '#050505'}]}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            path = Path(f.name)
        try:
            tokens = load_pencil_variables(path)
            self.assertEqual(tokens['bg'], '#050505')
        finally:
            path.unlink()


if __name__ == '__main__':
    unittest.main()
