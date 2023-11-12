import unittest
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._rectangle_utils import get_rectangles_enclosing_rectangle

class TestFunctionGetRectanglesEnclosingRectangle(unittest.TestCase):

    def test_multiple_rectangles(self):
        rectangles = [(1, 2, 3, 4), (2, 1, 4, 3), (-1, -1, 1, 2)]
        result = get_rectangles_enclosing_rectangle(rectangles)
        self.assertEqual(result, (-1, -1, 4, 4))

    def test_single_rectangle(self):
        rectangles = [(2, 1, 5, 6)]
        result = get_rectangles_enclosing_rectangle(rectangles)
        self.assertEqual(result, (2, 1, 5, 6))

    def test_empty_list(self):
        rectangles = []
        with self.assertRaises(IndexError):
            get_rectangles_enclosing_rectangle(rectangles)
