import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._assertions import assert_non_empty_hierarchy_formation
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._exceptions import EmptyConstructionStructureHierarchyFormationException


class TestFunctionAssertNonEmptyHierarchyFormation(unittest.TestCase):

    def test_not_raising(self):
        assert_non_empty_hierarchy_formation(
            hierarchy_formation=[OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER, ])

    def test_raising(self):
        with self.assertRaises(EmptyConstructionStructureHierarchyFormationException):
            assert_non_empty_hierarchy_formation(hierarchy_formation=[])
