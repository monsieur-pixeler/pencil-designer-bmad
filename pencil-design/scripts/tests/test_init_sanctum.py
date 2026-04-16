#!/usr/bin/env python3
"""Tests for init-sanctum.py scaffolding functions."""

import importlib.util
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


mod = load_module('init-sanctum')
parse_yaml_config = mod.parse_yaml_config
parse_frontmatter = mod.parse_frontmatter
discover_capabilities = mod.discover_capabilities
generate_capabilities_md = mod.generate_capabilities_md
substitute_vars = mod.substitute_vars


class TestParseYamlConfig(unittest.TestCase):
    def test_basic(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('user_name: Ramon\ncommunication_language: Dutch\n')
            path = Path(f.name)
        result = parse_yaml_config(path)
        self.assertEqual(result, {'user_name': 'Ramon', 'communication_language': 'Dutch'})

    def test_comments(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('# comment\nkey1: value1\n# another\nkey2: value2\n')
            path = Path(f.name)
        result = parse_yaml_config(path)
        self.assertEqual(result, {'key1': 'value1', 'key2': 'value2'})

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write('')
            path = Path(f.name)
        result = parse_yaml_config(path)
        self.assertEqual(result, {})

    def test_missing_file(self):
        result = parse_yaml_config(Path('/nonexistent/config.yaml'))
        self.assertEqual(result, {})

    def test_quoted_values(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("name: 'Ramon'\npath: \"/some/path\"\n")
            path = Path(f.name)
        result = parse_yaml_config(path)
        self.assertEqual(result, {'name': 'Ramon', 'path': '/some/path'})


class TestParseFrontmatter(unittest.TestCase):
    def test_valid(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write('---\nname: test-cap\ndescription: A test\ncode: TC\n---\n\n# Content\n')
            path = Path(f.name)
        result = parse_frontmatter(path)
        self.assertEqual(result['name'], 'test-cap')
        self.assertEqual(result['code'], 'TC')

    def test_no_frontmatter(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write('# Just markdown\n\nNo frontmatter.\n')
            path = Path(f.name)
        result = parse_frontmatter(path)
        self.assertEqual(result, {})

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write('')
            path = Path(f.name)
        result = parse_frontmatter(path)
        self.assertEqual(result, {})


class TestDiscoverCapabilities(unittest.TestCase):
    def test_finds_capabilities(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            refs = Path(tmpdir)
            (refs / 'test-cap.md').write_text(
                '---\nname: test-cap\ndescription: Test\ncode: TC\n---\n\n# Test\n'
            )
            (refs / 'no-code.md').write_text(
                '---\nname: no-code\ndescription: No code\n---\n\n# No\n'
            )
            (refs / 'first-breath.md').write_text(
                '---\nname: first-breath\ncode: FB\n---\n\n# FB\n'
            )
            caps = discover_capabilities(refs, './references')
        self.assertEqual(len(caps), 1)
        self.assertEqual(caps[0]['name'], 'test-cap')
        self.assertEqual(caps[0]['code'], 'TC')

    def test_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            caps = discover_capabilities(Path(tmpdir), './references')
        self.assertEqual(caps, [])


class TestGenerateCapabilitiesMd(unittest.TestCase):
    def test_correct_table(self):
        caps = [
            {'name': 'design', 'description': 'Design', 'code': 'DP', 'source': './ref/d.md'},
            {'name': 'audit', 'description': 'Audit', 'code': 'AA', 'source': './ref/a.md'},
        ]
        result = generate_capabilities_md(caps, evolvable=True)
        self.assertIn('## Built-in', result)
        self.assertIn('[AA]', result)
        self.assertIn('[DP]', result)
        # AA before DP (sorted)
        self.assertLess(result.index('[AA]'), result.index('[DP]'))

    def test_evolvable_flag(self):
        caps = [{'name': 'x', 'description': 'y', 'code': 'XY', 'source': 'z'}]
        self.assertIn('## Learned', generate_capabilities_md(caps, evolvable=True))
        self.assertNotIn('## Learned', generate_capabilities_md(caps, evolvable=False))

    def test_empty_caps(self):
        result = generate_capabilities_md([], evolvable=False)
        self.assertIn('## Built-in', result)


class TestSubstituteVars(unittest.TestCase):
    def test_basic(self):
        result = substitute_vars('Hello {user_name}!', {'user_name': 'Ramon'})
        self.assertEqual(result, 'Hello Ramon!')

    def test_missing_vars_untouched(self):
        result = substitute_vars('{known} and {unknown}', {'known': 'yes'})
        self.assertEqual(result, 'yes and {unknown}')

    def test_empty_variables(self):
        result = substitute_vars('Nothing {here}.', {})
        self.assertEqual(result, 'Nothing {here}.')

    def test_multiple_occurrences(self):
        result = substitute_vars('{x} likes {x}.', {'x': 'Pencil'})
        self.assertEqual(result, 'Pencil likes Pencil.')


if __name__ == '__main__':
    unittest.main()
