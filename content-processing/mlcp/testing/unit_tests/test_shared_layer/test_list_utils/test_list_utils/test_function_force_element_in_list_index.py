import unittest

from shared_layer.list_utils._list_utils import force_element_in_list_index


class TestFunctionForceElementInListIndex(unittest.TestCase):

    def test_single(self):
        list_ = []
        force_element_in_list_index(list_, 2, 1)
        self.assertEqual(list_, [None, None, 1])

    def test_multiple(self):
        list_ = []
        force_element_in_list_index(list_, 2, 1)
        force_element_in_list_index(list_, 4, 2)
        force_element_in_list_index(list_, 4, 3)
        self.assertEqual(list_, [None, None, 1, None, 3])

    def test_non_none_default(self):
        list_ = []
        force_element_in_list_index(list_, 2, 1, default=list)
        force_element_in_list_index(list_, 4, 2, default=list)
        force_element_in_list_index(list_, 4, 3, default=list)
        self.assertEqual(list_, [[], [], 1, [], 3])

    def test_with_long_list(self):
        list_ = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        force_element_in_list_index(list_, 2, 1)
        force_element_in_list_index(list_, 4, 2)
        force_element_in_list_index(list_, 4, 3)
        self.assertEqual(list_, [0, 1, 1, 3, 3, 5, 6, 7, 8, 9])
