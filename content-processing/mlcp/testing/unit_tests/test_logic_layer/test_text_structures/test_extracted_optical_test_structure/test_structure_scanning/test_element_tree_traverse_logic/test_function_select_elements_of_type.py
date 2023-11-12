import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure.structure_scanning._element_tree_traverse_logic import select_elements_of_type


class TestFunctionSelectElementsOfType(unittest.TestCase):

    def test_on_list_of_elements(self):

        elements = [
            OpticalTextStructureWord(),
            OpticalTextStructureLine(),
            OpticalTextStructureLine(),
            OpticalTextStructureElement(),
            OpticalTextStructureWord(),
            OpticalTextStructureElement(),
            OpticalTextStructureGroup(),
            OpticalTextStructureWord(),
            OpticalTextStructureWord(),
            OpticalTextStructureElement(),
            OpticalTextStructureGroup(),
            OpticalTextStructureLine(),
            OpticalTextStructureLine(),
            OpticalTextStructureElement()
        ]

        self.assertEqual(len(select_elements_of_type(elements, OpticalStructureHierarchyLevel.WORD)), 4)
        self.assertEqual(len(select_elements_of_type(elements, OpticalStructureHierarchyLevel.LINE)), 4)
        self.assertEqual(len(select_elements_of_type(elements, OpticalStructureHierarchyLevel.GROUP)), 2)

    def test_on_empty_list(self):
        elements = []

        self.assertEqual(len(select_elements_of_type(elements, OpticalStructureHierarchyLevel.WORD)), 0)
        self.assertEqual(len(select_elements_of_type(elements, OpticalStructureHierarchyLevel.LINE)), 0)
        self.assertEqual(len(select_elements_of_type(elements, OpticalStructureHierarchyLevel.GROUP)), 0)

    def test_non_elements_list(self):
        elements = [
            'hello',
            205,
            ('a', 'b', 'c')
        ]

        self.assertEqual(len(select_elements_of_type(elements, OpticalStructureHierarchyLevel.WORD)), 0)
        self.assertEqual(len(select_elements_of_type(elements, OpticalStructureHierarchyLevel.LINE)), 0)
        self.assertEqual(len(select_elements_of_type(elements, OpticalStructureHierarchyLevel.GROUP)), 0)
