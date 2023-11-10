import unittest
from logic_layer.text_structures.extracted_optical_text_structure._structure_calculations._geometry_calculations._rectangle_utils import get_rectangle_width

class TestFunctionGetRectangleWidth(unittest.TestCase):

    def test_positive_width(self):
        rect = (1, 2, 5, 6)
        expected_width = 4
        self.assertEqual(get_rectangle_width(rect), expected_width)

    def test_zero_width(self):
        rect = (3, 4, 3, 8)
        expected_width = 0
        self.assertEqual(get_rectangle_width(rect), expected_width)

    def test_negative_coordinates(self):
        rect = (-3, -4, -1, 2)
        expected_width = 2
        self.assertEqual(get_rectangle_width(rect), expected_width)
