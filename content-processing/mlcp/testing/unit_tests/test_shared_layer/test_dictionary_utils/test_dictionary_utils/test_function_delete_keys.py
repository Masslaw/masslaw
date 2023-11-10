import unittest

from shared_layer.dictionary_utils._dictionary_utils import delete_keys


class TestFunctionDeleteKeys(unittest.TestCase):

    def test_basic_functionality(self):
        d = {'a': 1, 'b': 2, 'c': 3}
        delete_keys(d, ['b'])
        self.assertEqual(d, {'a': 1, 'c': 3})

    def test_multiple_keys(self):
        d = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        delete_keys(d, ['a', 'c'])
        self.assertEqual(d, {'b': 2, 'd': 4})

    def test_nested_keys(self):
        d = {'a': {'b': 1, 'c': 2}, 'd': 3}
        delete_keys(d, [['a', 'b']])
        self.assertEqual(d, {'a': {'c': 2}, 'd': 3})

    def test_multiple_nested_keys(self):
        d = {'a': {'b': {'c': 1, 'd': 2}}, 'e': 3}
        delete_keys(d, [['a', 'b', 'c'], 'e'])
        self.assertEqual(d, {'a': {'b': {'d': 2}}})

    def test_non_existent_key(self):
        d = {'a': 1, 'b': 2}
        delete_keys(d, ['c'])
        self.assertEqual(d, {'a': 1, 'b': 2})

    def test_non_existent_nested_key(self):
        d = {'a': {'b': 1}}
        delete_keys(d, [['a', 'c']])
        self.assertEqual(d, {'a': {'b': 1}})

    def test_empty_keys(self):
        d = {'a': 1}
        delete_keys(d, [])
        self.assertEqual(d, {'a': 1})
