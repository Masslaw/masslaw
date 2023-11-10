import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureCharacter
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._assertions import assert_nested_child
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._exceptions import StructureConstructionElementNestingException


class TestFunctionAssertNestedChild(unittest.TestCase):

    def test_not_raising(self):
        hierarchy_formation = [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER]
        assert_nested_child(hierarchy_formation=hierarchy_formation, child_instance=OpticalTextStructureGroup())
        assert_nested_child(hierarchy_formation=hierarchy_formation, child_instance=OpticalTextStructureLine())
        assert_nested_child(hierarchy_formation=hierarchy_formation, child_instance=OpticalTextStructureWord())
        assert_nested_child(hierarchy_formation=hierarchy_formation, child_instance=OpticalTextStructureCharacter())

    def test_raising(self):
        with self.assertRaises(StructureConstructionElementNestingException):
            assert_nested_child(hierarchy_formation=[OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER],
                child_instance=OpticalTextStructureGroup())
