import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._geometry_calculations import get_average_gap_between_nested_child_elements


class TestFunctionGetAverageGapBetweenNestedChildElements(unittest.TestCase):

    def test_average_gap_with_nested_child_elements(self):
        element = OpticalTextStructureGroup(
            children=[
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(bounding_rect=(0, 0, 10, 10)),
                        OpticalTextStructureWord(bounding_rect=(15, 0, 25, 10))
                    ]
                ),
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(bounding_rect=(0, 20, 10, 30)),
                        OpticalTextStructureWord(bounding_rect=(20, 20, 30, 30))
                    ]
                ),
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(bounding_rect=(5, 40, 15, 50)),
                        OpticalTextStructureWord(bounding_rect=(25, 40, 35, 50))
                    ]
                ),
            ]
        )

        average_gap_width, average_gap_height = get_average_gap_between_nested_child_elements(element, OpticalStructureHierarchyLevel.WORD)

        expected_average_gap_width = 25 / 3
        expected_average_gap_height = 0

        self.assertEqual(average_gap_width, expected_average_gap_width)
        self.assertEqual(average_gap_height, expected_average_gap_height)
