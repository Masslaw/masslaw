import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyFormation
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure import optical_text_structure_exceptions
from logic_layer.text_structures.extracted_optical_text_structure._assertions import assert_hierarchy_formation


class TestFunctionAssertHierarchyFormation(unittest.TestCase):

    def test_assert_hierarchy_formation_normal(self):
        hierarchy_formation: OpticalStructureHierarchyFormation = [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD,
                                                                   OpticalStructureHierarchyLevel.CHARACTER]
        assert_hierarchy_formation(hierarchy_formation)

    def test_assert_hierarchy_formation_empty(self):
        hierarchy_formation: OpticalStructureHierarchyFormation = []
        with self.assertRaises(optical_text_structure_exceptions.EmptyStructureHierarchyFormationException):
            assert_hierarchy_formation(hierarchy_formation)

    def test_assert_hierarchy_formation_duplicates(self):
        hierarchy_formation: OpticalStructureHierarchyFormation = [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE,
                                                                   OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER]
        with self.assertRaises(optical_text_structure_exceptions.DuplicateLevelsInStructureHierarchyFormationException):
            assert_hierarchy_formation(hierarchy_formation)
