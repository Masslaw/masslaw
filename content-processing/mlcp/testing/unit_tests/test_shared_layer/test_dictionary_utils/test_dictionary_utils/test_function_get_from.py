import unittest

from shared_layer.dictionary_utils._dictionary_utils import get_from


class TestFunctionGetFrom(unittest.TestCase):

    def test_basic_functionality(self):
        d = {'a': {'b': {'c': 'value'}}}
        self.assertEqual(get_from(d, ['a', 'b', 'c']), 'value')

    def test_default_return_when_key_missing(self):
        d = {'a': {'b': {'c': 'value'}}}
        self.assertIsNone(get_from(d, ['a', 'b', 'd']))
        self.assertEqual(get_from(d, ['a', 'b', 'd'], default='missing'), 'missing')

    def test_default_return_with_non_dict_value(self):
        d = {'a': 'value'}
        self.assertIsNone(get_from(d, ['a', 'b']))
        self.assertEqual(get_from(d, ['a', 'b'], default='missing'), 'missing')

    def test_empty_path_returns_copy_of_original(self):
        d = {'a': {'b': {'c': 'value'}}}
        self.assertEqual(get_from(d, []), d.copy())

    def test_nonexistent_path(self):
        d = {'a': {'b': {'c': 'value'}}}
        self.assertIsNone(get_from(d, ['x', 'y']))
        self.assertEqual(get_from(d, ['x', 'y'], default='missing'), 'missing')

    def test_path_longer_than_depth(self):
        d = {'a': {'b': {'c': 'value'}}}
        self.assertIsNone(get_from(d, ['a', 'b', 'c', 'd']))
        self.assertEqual(get_from(d, ['a', 'b', 'c', 'd'], default='missing'), 'missing')
