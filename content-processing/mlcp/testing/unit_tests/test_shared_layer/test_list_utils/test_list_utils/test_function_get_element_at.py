import unittest

from shared_layer.list_utils._list_utils import get_element_at


class TestFunctionGetElementAt(unittest.TestCase):

    def test_normal(self):
        list_ = [1, 2, 3, 4]
        element = get_element_at(list_, 2)
        self.assertEqual(element, 3)

    def test_negative(self):
        list_ = [1, 2, 3, 4]
        element = get_element_at(list_, -1)
        self.assertEqual(element, 4)

    def test_out_of_range(self):
        list_ = [1, 2, 3, 4]
        element = get_element_at(list_, 10)
        self.assertEqual(element, None)

    def test_default(self):
        list_ = [1, 2, 3, 4]
        element = get_element_at(list_, 10, default=0)
        self.assertEqual(element, 0)
