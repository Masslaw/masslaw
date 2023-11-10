import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureCharacter
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import hierarchy_level_to_element_class
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement


class TestFunctionHierarchyLevelToElementClass(unittest.TestCase):

    def test_on_valid_hierarchy_levels(self):
        self.assertEqual(hierarchy_level_to_element_class(OpticalStructureHierarchyLevel.GROUP), OpticalTextStructureGroup)
        self.assertEqual(hierarchy_level_to_element_class(OpticalStructureHierarchyLevel.LINE), OpticalTextStructureLine)
        self.assertEqual(hierarchy_level_to_element_class(OpticalStructureHierarchyLevel.WORD), OpticalTextStructureWord)
        self.assertEqual(hierarchy_level_to_element_class(OpticalStructureHierarchyLevel.CHARACTER), OpticalTextStructureCharacter)

    def test_on_invalid_hierarchy_level(self):
        self.assertEqual(hierarchy_level_to_element_class('invalid'), OpticalTextStructureElement)
