import unittest

from shared_layer.dictionary_utils._dictionary_utils import delete_nested_keys


class TestFunctionDeleteNestedKeys(unittest.TestCase):

    def test_basic_functionality(self):
        d = {'a': 1, 'b': 2, 'c': 3}
        delete_nested_keys(d, 'b')
        self.assertEqual(d, {'a': 1, 'c': 3})

    def test_nested_dictionaries(self):
        d = {'a': {'b': 1, 'c': 2}, 'b': 3}
        delete_nested_keys(d, 'b')
        self.assertEqual(d, {'a': {'c': 2}})

    def test_deeply_nested_dictionaries(self):
        d = {'a': {'b': {'c': {'b': 1}}, 'd': 2}, 'e': {'b': 3}}
        delete_nested_keys(d, 'b')
        self.assertEqual(d, {'a': {'d': 2}, 'e': {}})

    def test_list_inside_dictionary(self):
        d = {'a': [{'b': 1}, {'c': 2, 'b': 3}]}
        delete_nested_keys(d, 'b')
        self.assertEqual(d, {'a': [{}, {'c': 2}]})

    def test_no_matching_key(self):
        d = {'a': 1, 'c': 2}
        delete_nested_keys(d, 'b')
        self.assertEqual(d, {'a': 1, 'c': 2})

    def test_empty_dictionary(self):
        d = {}
        delete_nested_keys(d, 'b')
        self.assertEqual(d, {})
