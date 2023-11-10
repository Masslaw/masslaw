import unittest

from shared_layer.dictionary_utils._dictionary_utils import set_at


class TestFunctionSetAt(unittest.TestCase):

    def test_basic_functionality(self):
        d = {}
        set_at(d, ['a', 'b', 'c'], 'value')
        self.assertEqual(d, {'a': {'b': {'c': 'value'}}})

    def test_overwrite_existing_value(self):
        d = {'a': {'b': {'c': 'old_value'}}}
        set_at(d, ['a', 'b', 'c'], 'new_value')
        self.assertEqual(d, {'a': {'b': {'c': 'new_value'}}})

    def test_extend_existing_path(self):
        d = {'a': {'b': {}}}
        set_at(d, ['a', 'b', 'c'], 'value')
        self.assertEqual(d, {'a': {'b': {'c': 'value'}}})

    def test_single_key_path(self):
        d = {}
        set_at(d, ['a'], 'value')
        self.assertEqual(d, {'a': 'value'})

    def test_overwrite_non_dict_element(self):
        d = {'a': 'old_value'}
        set_at(d, ['a', 'b'], 'value')
        self.assertEqual(d, {'a': {'b': 'value'}})
