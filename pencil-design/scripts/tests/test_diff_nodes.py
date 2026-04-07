#!/usr/bin/env python3
"""Unit tests for diff-nodes.py"""

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


mod = load_module('diff-nodes')
flatten_tree = mod.flatten_tree
diff_node_properties = mod.diff_node_properties
diff_trees = mod.diff_trees
compare_value = mod.compare_value


class TestFlattenTree(unittest.TestCase):
    def test_single_node(self):
        node = {'name': 'Frame', 'type': 'frame', 'children': []}
        flat = flatten_tree(node)
        self.assertIn('Frame', flat)

    def test_nested_children(self):
        node = {
            'name': 'Root',
            'type': 'frame',
            'children': [
                {'name': 'Header', 'type': 'frame', 'children': []},
                {'name': 'Body', 'type': 'frame', 'children': [
                    {'name': 'Text', 'type': 'text', 'children': []},
                ]},
            ],
        }
        flat = flatten_tree(node)
        self.assertIn('Root', flat)
        self.assertIn('Root/Header', flat)
        self.assertIn('Root/Body', flat)
        self.assertIn('Root/Body/Text', flat)

    def test_node_without_name_uses_id(self):
        node = {'id': 'abc123', 'type': 'frame', 'children': []}
        flat = flatten_tree(node)
        self.assertIn('abc123', flat)


class TestCompareValue(unittest.TestCase):
    def test_equal_strings(self):
        self.assertTrue(compare_value('#F4F4F5', '#F4F4F5'))

    def test_different_strings(self):
        self.assertFalse(compare_value('#F4F4F5', '#F5F5F5'))

    def test_float_within_tolerance(self):
        self.assertTrue(compare_value(24.0, 24.3))

    def test_float_outside_tolerance(self):
        self.assertFalse(compare_value(24.0, 25.0))

    def test_dict_equal(self):
        self.assertTrue(compare_value({'a': 1, 'b': 2}, {'a': 1, 'b': 2}))

    def test_dict_different(self):
        self.assertFalse(compare_value({'a': 1}, {'a': 2}))

    def test_none_vs_none(self):
        self.assertTrue(compare_value(None, None))

    def test_none_vs_value(self):
        self.assertFalse(compare_value(None, 'something'))


class TestDiffNodeProperties(unittest.TestCase):
    def test_no_changes(self):
        before = {'fill': '#000000', 'fontSize': 16}
        after = {'fill': '#000000', 'fontSize': 16}
        changes = diff_node_properties(before, after, include_position=False)
        self.assertEqual(len(changes), 0)

    def test_fill_changed(self):
        before = {'fill': '#000000'}
        after = {'fill': '#FFFFFF'}
        changes = diff_node_properties(before, after, include_position=False)
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]['property'], 'fill')
        self.assertEqual(changes[0]['before'], '#000000')
        self.assertEqual(changes[0]['after'], '#FFFFFF')

    def test_position_excluded(self):
        before = {'x': 0, 'y': 0, 'fill': '#000000'}
        after = {'x': 100, 'y': 50, 'fill': '#000000'}
        changes = diff_node_properties(before, after, include_position=False)
        self.assertEqual(len(changes), 0)

    def test_position_included(self):
        before = {'x': 0}
        after = {'x': 100}
        changes = diff_node_properties(before, after, include_position=True)
        self.assertEqual(len(changes), 1)

    def test_content_change(self):
        before = {'content': 'Hello'}
        after = {'content': 'World'}
        changes = diff_node_properties(before, after, include_position=False)
        self.assertEqual(len(changes), 1)
        self.assertEqual(changes[0]['property'], 'content')


class TestDiffTrees(unittest.TestCase):
    def make_frame(self, name, fill='#000000', children=None):
        return {
            'name': name,
            'type': 'frame',
            'fill': fill,
            'children': children or [],
        }

    def test_no_changes(self):
        tree = self.make_frame('Root', fill='#F4F4F5')
        result = diff_trees(tree, tree, include_position=False)
        self.assertEqual(result['status'], 'no_changes')
        self.assertEqual(result['summary']['total'], 0)

    def test_added_child(self):
        before = self.make_frame('Root', children=[])
        after = self.make_frame('Root', children=[self.make_frame('NewChild')])
        result = diff_trees(before, after, include_position=False)
        self.assertEqual(result['summary']['added'], 1)
        self.assertEqual(result['status'], 'changed')

    def test_removed_child(self):
        before = self.make_frame('Root', children=[self.make_frame('OldChild')])
        after = self.make_frame('Root', children=[])
        result = diff_trees(before, after, include_position=False)
        self.assertEqual(result['summary']['removed'], 1)
        self.assertEqual(result['status'], 'changed')

    def test_property_change(self):
        before = self.make_frame('Root', fill='#000000')
        after = self.make_frame('Root', fill='#FFFFFF')
        result = diff_trees(before, after, include_position=False)
        self.assertEqual(result['summary']['changed'], 1)
        self.assertEqual(result['changed'][0]['changes'][0]['property'], 'fill')

    def test_unchanged_children_not_reported(self):
        child = self.make_frame('Child', fill='#AAAAAA')
        before = self.make_frame('Root', children=[child])
        after = self.make_frame('Root', children=[child])
        result = diff_trees(before, after, include_position=False)
        self.assertEqual(result['summary']['total'], 0)


if __name__ == '__main__':
    unittest.main()
