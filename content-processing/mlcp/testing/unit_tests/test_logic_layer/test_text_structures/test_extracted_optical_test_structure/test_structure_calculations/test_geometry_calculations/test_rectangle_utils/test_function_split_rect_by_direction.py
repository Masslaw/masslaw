import unittest
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._rectangle_utils import split_rect_by_direction
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureElementOrderDirection

class TestFunctionSplitRectByDirection(unittest.TestCase):

    def test_split_horizontal(self):
        rect = (0, 0, 10, 5)
        expected = [(0, 0, 5, 5), (5, 0, 10, 5)]
        result = split_rect_by_direction(rect, OpticalStructureElementOrderDirection.HORIZONTAL, 2)
        self.assertEqual(result, expected)

    def test_split_vertical(self):
        rect = (0, 0, 5, 10)
        expected = [(0, 0, 5, 5), (0, 5, 5, 10)]
        result = split_rect_by_direction(rect, OpticalStructureElementOrderDirection.VERTICAL, 2)
        self.assertEqual(result, expected)

    def test_invalid_direction(self):
        rect = (0, 0, 10, 5)
        expected = [rect]
        result = split_rect_by_direction(rect, "invalid_direction", 2)
        self.assertEqual(result, expected)

    def test_no_split(self):
        rect = (2, 2, 5, 6)
        expected = [rect]
        result = split_rect_by_direction(rect, OpticalStructureElementOrderDirection.HORIZONTAL, 1)
        self.assertEqual(result, expected)
