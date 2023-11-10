import unittest

from shared_layer.dictionary_utils._dictionary_utils import remove_not_provided


class TestFunctionRemoveNotProvided(unittest.TestCase):

    def test_basic_functionality(self):
        d = {'a': 1, 'b': None, 'c': ''}
        remove_not_provided(d)
        self.assertEqual(d, {'a': 1})

    def test_nested_dicts(self):
        d = {'a': {'b': 'value', 'c': None}, 'd': ''}
        remove_not_provided(d)
        self.assertEqual(d, {'a': {'b': 'value'}})

    def test_remove_empty_nested_dicts(self):
        d = {'a': {'b': None}, 'c': 2}
        remove_not_provided(d)
        self.assertEqual(d, {'c': 2})

    def test_no_removals(self):
        d = {'a': 1, 'b': 2}
        remove_not_provided(d)
        self.assertEqual(d, {'a': 1, 'b': 2})

    def test_deeply_nested_dicts(self):
        d = {'a': {'b': {'c': {'d': None}}}, 'e': 'value'}
        remove_not_provided(d)
        self.assertEqual(d, {'e': 'value'})
