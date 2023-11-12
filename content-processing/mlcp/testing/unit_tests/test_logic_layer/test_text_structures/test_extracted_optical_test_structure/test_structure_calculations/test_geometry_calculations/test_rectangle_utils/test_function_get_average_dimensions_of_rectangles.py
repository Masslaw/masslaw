import unittest
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._rectangle_utils import get_average_dimensions_of_rectangles

class TestFunctionGetAverageDimensionsOfRectangles(unittest.TestCase):

    def test_multiple_rectangles(self):
        rectangles = [(0, 0, 4, 4), (2, 2, 6, 6)]
        expected_average_width = 4.0
        expected_average_height = 4.0
        average_width, average_height = get_average_dimensions_of_rectangles(rectangles)
        self.assertEqual(average_width, expected_average_width)
        self.assertEqual(average_height, expected_average_height)

    def test_single_rectangle(self):
        rectangles = [(0, 0, 3, 5)]
        expected_average_width = 3.0
        expected_average_height = 5.0
        average_width, average_height = get_average_dimensions_of_rectangles(rectangles)
        self.assertEqual(average_width, expected_average_width)
        self.assertEqual(average_height, expected_average_height)

    def test_no_rectangles(self):
        rectangles = []
        expected_average_width = 0.0
        expected_average_height = 0.0
        average_width, average_height = get_average_dimensions_of_rectangles(rectangles)
        self.assertEqual(average_width, expected_average_width)
        self.assertEqual(average_height, expected_average_height)

    def test_irregular_rectangles(self):
        rectangles = [(2, 2, 5, 7), (1, 1, 3, 3), (0, 0, 2, 5)]
        expected_average_width = 7 / 3
        expected_average_height = 12 / 3
        average_width, average_height = get_average_dimensions_of_rectangles(rectangles)
        self.assertEqual(average_width, expected_average_width)
        self.assertAlmostEqual(average_height, expected_average_height)
