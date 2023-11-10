import unittest

from shared_layer.dictionary_utils._dictionary_utils import check_structure


class TestFunctionCheckStructure(unittest.TestCase):

    def test_basic_structure(self):
        d = {'a': 1, 'b': 'test', 'c': 3.5}
        validation = {'a': int, 'b': str, 'c': float}
        self.assertTrue(check_structure(d, validation))

    def test_invalid_basic_structure(self):
        d = {'a': 'test', 'b': 2, 'c': 3.5}
        validation = {'a': int, 'b': str, 'c': float}
        self.assertFalse(check_structure(d, validation))

    def test_nested_structure(self):
        d = {'a': {'x': 1, 'y': 'hello'}, 'b': 2}
        validation = {'a': {'x': int, 'y': str}, 'b': int}
        self.assertTrue(check_structure(d, validation))

    def test_invalid_nested_structure(self):
        d = {'a': {'x': 'test', 'y': 'hello'}, 'b': 2}
        validation = {'a': {'x': int, 'y': str}, 'b': int}
        self.assertFalse(check_structure(d, validation))

    def test_with_list_validation(self):
        d = {'a': 1, 'b': 'test'}
        validation = {'a': [int, None], 'b': [str, None]}
        self.assertTrue(check_structure(d, validation))

    def test_with_none_in_dict(self):
        d = {'a': None, 'b': 'test'}
        validation = {'a': [int, None], 'b': [str, None]}
        self.assertTrue(check_structure(d, validation))

    def test_missing_key(self):
        d = {'a': 1}
        validation = {'a': int, 'b': str}
        self.assertFalse(check_structure(d, validation))

    def test_extra_key(self):
        d = {'a': 1, 'b': 'test', 'c': 3.5}
        validation = {'a': int, 'b': str}
        self.assertTrue(check_structure(d, validation))
