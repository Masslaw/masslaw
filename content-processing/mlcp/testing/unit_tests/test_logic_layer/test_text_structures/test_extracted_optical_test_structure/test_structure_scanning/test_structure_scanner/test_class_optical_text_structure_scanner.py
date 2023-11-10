import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure._structure_scanning import OpticalTextStructureScanner

class TestClassOpticalTextStructureScanner(unittest.TestCase):

    def test_children_collecting(self):
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

        scanner = OpticalTextStructureScanner(element)

        nested_words = scanner.collect_all_nested_children_of_type(OpticalStructureHierarchyLevel.WORD)
        nested_lines = scanner.collect_all_nested_children_of_type(OpticalStructureHierarchyLevel.LINE)

        self.assertEqual(len(nested_words), 6)
        self.assertEqual(len(nested_lines), 2)

    def test_count_children(self):
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

        scanner = OpticalTextStructureScanner(element)

        nested_words_count = scanner.count_all_nested_children_of_type(OpticalStructureHierarchyLevel.WORD)
        nested_lines_count = scanner.count_all_nested_children_of_type(OpticalStructureHierarchyLevel.LINE)

        self.assertEqual(nested_words_count, 6)
        self.assertEqual(nested_lines_count, 2)
