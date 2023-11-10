import unittest

from shared_layer.list_utils._list_utils import force_element_in_index_path


class TestFunctionForceElementInIndexPath(unittest.TestCase):

    def test_single(self):
        list_ = []
        force_element_in_index_path(list_, [0, 1, 2, 3], 1)
        self.assertEqual(list_, [[None, [None, None, [None, None, None, 1]]]])

    def test_multiple(self):
        list_ = []
        force_element_in_index_path(list_, [0, 1, 2, 3], 1)
        force_element_in_index_path(list_, [0, 1, 2, 4], 2)
        force_element_in_index_path(list_, [0, 1, 3, 4], 3)
        self.assertEqual(list_, [[None, [None, None, [None, None, None, 1, 2], [None, None, None, None, 3]]]])

    def test_non_none_default(self):
        list_ = []
        force_element_in_index_path(list_, [0, 1, 2, 3], 1, default=list)
        force_element_in_index_path(list_, [0, 1, 2, 4], 2, default=list)
        force_element_in_index_path(list_, [0, 1, 3, 4], 3, default=list)
        self.assertEqual(list_, [[[], [[], [], [[], [], [], 1, 2], [[], [], [], [], 3]]]])
