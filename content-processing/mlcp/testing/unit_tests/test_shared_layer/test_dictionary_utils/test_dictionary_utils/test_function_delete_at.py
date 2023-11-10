import unittest

from shared_layer.dictionary_utils._dictionary_utils import delete_at


class TestFunctionDeleteAt(unittest.TestCase):

    def test_basic_functionality(self):
        d = {'a': 1, 'b': 2, 'c': 3}
        delete_at(d, ['b'])
        self.assertEqual(d, {'a': 1, 'c': 3})

    def test_nested_dictionaries(self):
        d = {'a': {'b': 1, 'c': 2}, 'd': 3}
        delete_at(d, ['a', 'b'])
        self.assertEqual(d, {'a': {'c': 2}, 'd': 3})

    def test_deeply_nested_dictionaries(self):
        d = {'a': {'b': {'c': 1, 'd': 2}}}
        delete_at(d, ['a', 'b', 'c'])
        self.assertEqual(d, {'a': {'b': {'d': 2}}})

    def test_non_existent_key(self):
        d = {'a': 1, 'b': 2}
        delete_at(d, ['c'])
        self.assertEqual(d, {'a': 1, 'b': 2})

    def test_non_existent_nested_key(self):
        d = {'a': {'b': 1}}
        delete_at(d, ['a', 'c'])
        self.assertEqual(d, {'a': {'b': 1}})

    def test_empty_path(self):
        d = {'a': 1}
        delete_at(d, [])
        self.assertEqual(d, {'a': 1})

    def test_path_to_non_dict(self):
        d = {'a': 1, 'b': [2, 3, 4]}
        delete_at(d, ['b', 1])
        self.assertEqual(d, {'a': 1, 'b': [2, 3, 4]})
