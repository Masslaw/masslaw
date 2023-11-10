import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure._structure_calculations._geometry_calculations._geometry_calculations import get_average_gap_between_elements


class TestFunctionGetAverageGapBetweenElements(unittest.TestCase):

    def test_average_gap_calculation(self):
        elements = [
            OpticalTextStructureWord(bounding_rect=(0, 0, 10, 10)),
            OpticalTextStructureWord(bounding_rect=(15, 0, 25, 10)),
            OpticalTextStructureWord(bounding_rect=(40, 0, 50, 10)),
        ]

        average_gap_width, average_gap_height = get_average_gap_between_elements(elements)

        expected_average_gap_width = 10
        expected_average_gap_height = 0

        self.assertEqual(average_gap_width, expected_average_gap_width)
        self.assertEqual(average_gap_height, expected_average_gap_height)
