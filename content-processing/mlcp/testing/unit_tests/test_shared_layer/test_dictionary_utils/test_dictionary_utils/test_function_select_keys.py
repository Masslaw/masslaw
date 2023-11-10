import unittest

from shared_layer.dictionary_utils._dictionary_utils import select_keys


class TestFunctionSelectKeys(unittest.TestCase):

    def test_basic_selection(self):
        d = {'a': 1, 'b': 2, 'c': {'d': 3}}
        selected = select_keys(d, ['a', 'c'])
        self.assertEqual(selected, {'a': 1, 'c': {'d': 3}})

    def test_nested_selection(self):
        d = {'a': {'b': {'c': 'value'}}}
        selected = select_keys(d, [['a', 'b', 'c']])
        self.assertEqual(selected, {'a': {'b': {'c': 'value'}}})

    def test_missing_keys(self):
        d = {'a': 1, 'b': 2}
        selected = select_keys(d, ['a', 'z'])
        self.assertEqual(selected, {'a': 1})

    def test_empty_keys_list(self):
        d = {'a': 1, 'b': 2}
        selected = select_keys(d, [])
        self.assertEqual(selected, {})

    def test_mixed_key_types(self):
        d = {'a': {'b': 1}, 'c': 2}
        selected = select_keys(d, ['c', ['a', 'b']])
        self.assertEqual(selected, {'a': {'b': 1}, 'c': 2})
