import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure._structure_scanning._element_tree_traverse_logic import collect_all_nested_children_of_type


class TestFunctionCollectAllNestedChildrenOfType(unittest.TestCase):

    def test_on_normal_structure(self):
        element = OpticalTextStructureGroup(
            children=[
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(list("word1")),
                        OpticalTextStructureWord(list("word2")),
                        OpticalTextStructureWord(list("word3"))
                    ]
                ),
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(list("word4")),
                        OpticalTextStructureWord(list("word5")),
                        OpticalTextStructureWord(list("word6"))
                    ]
                )
            ]
        )

        self.assertEqual(len(collect_all_nested_children_of_type(element, OpticalStructureHierarchyLevel.WORD)), 6)
        self.assertEqual(len(collect_all_nested_children_of_type(element, OpticalStructureHierarchyLevel.LINE)), 2)

    def test_on_empty_structure(self):
        element = OpticalTextStructureGroup()

        self.assertEqual(len(collect_all_nested_children_of_type(element, OpticalStructureHierarchyLevel.WORD)), 0)
        self.assertEqual(len(collect_all_nested_children_of_type(element, OpticalStructureHierarchyLevel.LINE)), 0)

    def test_on_root_element(self):
        element = OpticalTextStructureGroup(
            children=[
                OpticalTextStructureLine(),
                OpticalTextStructureLine(),
            ]
        )

        self.assertEqual(len(collect_all_nested_children_of_type(element, OpticalStructureHierarchyLevel.GROUP)), 0)
