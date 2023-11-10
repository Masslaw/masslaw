import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure._structure_calculations import StructureGeometryCalculator
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement


class TestClassStructureGeometryCalculator(unittest.TestCase):

    def test_calculate_bounding_rect_on_element_with_children(self):
        element = OpticalTextStructureElement(
            children=[
                OpticalTextStructureElement(bounding_rect=(0, 0, 10, 10)),
                OpticalTextStructureElement(bounding_rect=(10, 10, 20, 20)),
                OpticalTextStructureElement(bounding_rect=(20, 20, 30, 30)),
                OpticalTextStructureElement(bounding_rect=(30, 30, 40, 40)),
            ]
        )
        calculator = StructureGeometryCalculator(element)
        self.assertEqual(calculator.calculate_bounding_rect(), (0, 0, 40, 40))

    def test_calculate_element_children_average_size_on_element_with_children(self):
        element = OpticalTextStructureElement(
            children=[
                OpticalTextStructureElement(bounding_rect=(0, 0, 10, 10)),
                OpticalTextStructureElement(bounding_rect=(10, 10, 20, 20)),
                OpticalTextStructureElement(bounding_rect=(20, 20, 30, 30)),
                OpticalTextStructureElement(bounding_rect=(30, 30, 40, 40)),
            ]
        )
        calculator = StructureGeometryCalculator(element)
        size = calculator.calculate_element_children_average_size()
        self.assertEqual(size, (10, 10))

    def test_calculate_element_nested_children_average_size(self):
        element = OpticalTextStructureGroup(
            children=[
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(bounding_rect=(0,0, 10, 10)),
                        OpticalTextStructureWord(bounding_rect=(10, 0, 20, 10))
                    ]
                ),
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(bounding_rect=(0,0, 20, 20)),
                        OpticalTextStructureWord(bounding_rect=(20, 0, 40, 20))
                    ]
                )
            ]
        )

        calculator = StructureGeometryCalculator(element)

        size = calculator.calculate_element_nested_children_average_size(OpticalStructureHierarchyLevel.LINE)
        self.assertEqual(size, (30, 15))
        size = calculator.calculate_element_nested_children_average_size(OpticalStructureHierarchyLevel.WORD)
        self.assertEqual(size, (15, 15))

    def test_calculate_average_gap_between_child_elements(self):
        element = OpticalTextStructureGroup(
            children=[
                OpticalTextStructureLine(bounding_rect=(0, 0, 100, 10)),
                OpticalTextStructureLine(bounding_rect=(20, 20, 150, 30)),
                OpticalTextStructureLine(bounding_rect=(60, 50, 200, 60)),
            ]
        )

        calculator = StructureGeometryCalculator(element)

        gap = calculator.calculate_average_gap_between_child_elements()
        self.assertEqual(gap, (0, 15))

    def test_calculate_average_gap_between_nested_child_elements(self):
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

        calculator = StructureGeometryCalculator(element)

        gap = calculator.calculate_average_gap_between_nested_child_elements(OpticalStructureHierarchyLevel.LINE)
        self.assertEqual(gap, (0, 15))
        gap = calculator.calculate_average_gap_between_nested_child_elements(OpticalStructureHierarchyLevel.WORD)
        self.assertEqual(gap, (20, 0))
