import unittest

from shared_layer.list_utils._list_utils import set_list_length


class TestFunctionSetListLength(unittest.TestCase):

    def test_empty_to_long(self):
        list_ = []
        list_ = set_list_length(list_, 10)
        self.assertEqual(list_, [None] * 10)

    def test_non_empty_extended(self):
        list_ = [1, 2, 3, 4]
        list_ = set_list_length(list_, 10)
        self.assertEqual(list_, [1, 2, 3, 4, None, None, None, None, None, None])

    def test_long_to_short(self):
        list_ = [1, 2, 3, 4]
        list_ = set_list_length(list_, 2)
        self.assertEqual(list_, [1, 2])

    def test_non_empty_to_empty(self):
        list_ = [1, 2, 3, 4]
        list_ = set_list_length(list_, 0)
        self.assertEqual(list_, [])

    def test_extended_with_default(self):
        list_ = [1, 2, 3 ,4]
        list_ = set_list_length(list_, 10, default=list)
        self.assertEqual(list_, [1, 2, 3, 4, [], [], [], [], [], []])
