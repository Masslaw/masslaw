import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._geometry_calculations import get_element_children_average_size
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement


class TestFunctionGetElementChildrenAverageSize(unittest.TestCase):

    def test_average_size_no_children(self):
        element = OpticalTextStructureElement(children=[])
        width, height = get_element_children_average_size(element)
        self.assertEqual((width, height), (0, 0))

    def test_average_size_with_children(self):
        element = OpticalTextStructureGroup(
            children=[
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(bounding_rect=(0, 0, 10, 10)),
                        OpticalTextStructureWord(bounding_rect=(20, 0, 30, 10))
                    ]
                ),
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(bounding_rect=(0, 20, 10, 30)),
                        OpticalTextStructureWord(bounding_rect=(30, 20, 40, 30))
                    ]
                ),
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(bounding_rect=(0, 50, 10, 60)),
                        OpticalTextStructureWord(bounding_rect=(40, 50, 50, 60))
                    ]
                ),
            ]
        )
        expected_average_width = 40
        expected_average_height = 10

        average_width, average_height = get_element_children_average_size(element)

        self.assertEqual(average_width, expected_average_width)
        self.assertEqual(average_height, expected_average_height)
