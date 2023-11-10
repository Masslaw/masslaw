import unittest
from logic_layer.text_structures.extracted_optical_text_structure._structure_calculations._geometry_calculations._rectangle_utils import get_rectangle_height

class TestFunctionGetRectangleHeight(unittest.TestCase):

    def test_positive_height(self):
        rect = (1, 2, 5, 6)
        expected_height = 4
        self.assertEqual(get_rectangle_height(rect), expected_height)

    def test_zero_height(self):
        rect = (3, 4, 7, 4)
        expected_height = 0
        self.assertEqual(get_rectangle_height(rect), expected_height)

    def test_negative_coordinates(self):
        rect = (-3, -4, 1, -2)
        expected_height = 2
        self.assertEqual(get_rectangle_height(rect), expected_height)
