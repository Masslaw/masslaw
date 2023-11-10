import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._construction._construction_logic import append_children_to_element
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._exceptions import StructureConstructionInvalidElementTypeException


class TestFunctionAppendChildrenToElement(unittest.TestCase):

    def test_on_empty_element_with_correct_type(self):
        group = OpticalTextStructureGroup()
        group.set_children([])

        lines = [OpticalTextStructureLine() for _ in range(5)]

        append_children_to_element(group, lines)

        self.assertEqual(len(group.get_children()), 5)

    def test_on_non_empty_element_with_correct_type(self):
        group = OpticalTextStructureGroup()
        group.set_children([OpticalTextStructureLine() for _ in range(3)])

        lines = [OpticalTextStructureLine() for _ in range(5)]

        append_children_to_element(group, lines)

        self.assertEqual(len(group.get_children()), 8)

    def test_incorrect_type(self):
        group = OpticalTextStructureGroup()
        group.set_children([OpticalTextStructureLine()])

        words = [OpticalTextStructureWord() for _ in range(5)]

        with self.assertRaises(StructureConstructionInvalidElementTypeException):
            append_children_to_element(group, words)
