import unittest

from shared_layer.dictionary_utils._dictionary_utils import ensure_flat


class TestFunctionEnsureFlat(unittest.TestCase):

    def test_basic_functionality(self):
        d = {'a': {'b': 1, 'c': 2}, 'd': 3}
        ensure_flat(d)
        self.assertEqual(d, {'a': '{"b": 1, "c": 2}', 'd': 3})

    def test_list_values(self):
        d = {'a': [{'b': 1}, 2, {'c': 3}]}
        ensure_flat(d)
        self.assertEqual(d, {'a': ['{"b": 1}', 2, '{"c": 3}']})

    def test_list_of_non_dicts(self):
        d = {'a': [1, 2, 3]}
        ensure_flat(d)
        self.assertEqual(d, {'a': [1, 2, 3]})

    def test_empty_dict(self):
        d = {}
        ensure_flat(d)
        self.assertEqual(d, {})

    def test_nested_dicts_in_lists(self):
        d = {'a': [{'b': {'c': 1}}, 2, {'d': 3}]}
        ensure_flat(d)
        self.assertEqual(d, {'a': ['{"b": {"c": 1}}', 2, '{"d": 3}']})

    def test_non_dict_non_list_value(self):
        d = {'a': 'value'}
        ensure_flat(d)
        self.assertEqual(d, {'a': 'value'})
