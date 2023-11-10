import unittest

from logic_layer.text_structures.extracted_optical_text_structure._exceptions import DuplicateLevelsInStructureHierarchyFormationException
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure._exceptions import EmptyStructureHierarchyFormationException
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalStructureHierarchyLevel


class TestOpticalTextStructureRoot(unittest.TestCase):

    def test_hierarchy_formation_assertion_valid(self):
        hierarchy_levels = [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER]
        root = OpticalTextStructureRoot(hierarchy_formation=hierarchy_levels)
        self.assertEqual(root.get_hierarchy_formation(), hierarchy_levels)

    def test_hierarchy_formation_assertion_empty(self):
        invalid_hierarchy_levels = []
        with self.assertRaises(EmptyStructureHierarchyFormationException):
            OpticalTextStructureRoot(hierarchy_formation=invalid_hierarchy_levels)

    def test_hierarchy_formation_assertion_duplicates(self):
        invalid_hierarchy_levels = [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.CHARACTER]
        with self.assertRaises(DuplicateLevelsInStructureHierarchyFormationException):
            OpticalTextStructureRoot(hierarchy_formation=invalid_hierarchy_levels)

    def test_children_setting_and_retrieval(self):
        hierarchy_levels = [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER]
        root = OpticalTextStructureRoot(hierarchy_formation=hierarchy_levels)

        self.assertEqual(root.get_children(), [])

        children_elements = [OpticalTextStructureGroup(), OpticalTextStructureGroup()]
        root.set_children(children_elements)
        self.assertEqual(root.get_children(), children_elements)

    def test_hierarchy_formation_retrieval(self):
        hierarchy_levels = [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER]
        root = OpticalTextStructureRoot(hierarchy_formation=hierarchy_levels)
        self.assertEqual(root.get_hierarchy_formation(), hierarchy_levels)
