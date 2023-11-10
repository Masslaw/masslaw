import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureParagraph
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._construction._construction_logic import get_appropriate_element_for_entry_in_structure_hierarchy

structure_hierarchy = [OpticalStructureHierarchyLevel.PARAGRAPH, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER]


class TestFunctionGetAppropriateElementForEntryInStructureHierarchy(unittest.TestCase):

    def test_with_paragraph(self):
        entry = ('This is\na paragraph', (0, 0, 100, 20))

        paragraph = get_appropriate_element_for_entry_in_structure_hierarchy(entry=entry, hierarchy_formation=structure_hierarchy)

        self.assertEqual(paragraph.__class__, OpticalTextStructureParagraph)
        self.assertEqual(len(paragraph.get_children()), 2)
        self.assertEqual(len(paragraph.get_children()[0].get_children()), 2)
        self.assertEqual(len(paragraph.get_children()[0].get_children()[0].get_children()), 4)
        self.assertEqual(len(paragraph.get_children()[0].get_children()[1].get_children()), 2)
        self.assertEqual(len(paragraph.get_children()[1].get_children()), 2)
        self.assertEqual(len(paragraph.get_children()[1].get_children()[0].get_children()), 1)
        self.assertEqual(len(paragraph.get_children()[1].get_children()[1].get_children()), 9)

    def test_with_line(self):
        entry = ('this is a line', (0, 0, 100, 10))

        line = get_appropriate_element_for_entry_in_structure_hierarchy(entry=entry, hierarchy_formation=structure_hierarchy)

        self.assertEqual(line.__class__, OpticalTextStructureLine)
        self.assertEqual(len(line.get_children()), 4)
        self.assertEqual(len(line.get_children()[0].get_children()), 4)
        self.assertEqual(len(line.get_children()[1].get_children()), 2)
        self.assertEqual(len(line.get_children()[2].get_children()), 1)
        self.assertEqual(len(line.get_children()[3].get_children()), 4)

    def test_with_word(self):
        entry = ('word', (0, 0, 40, 10))

        word = get_appropriate_element_for_entry_in_structure_hierarchy(entry=entry, hierarchy_formation=structure_hierarchy)

        self.assertEqual(word.__class__, OpticalTextStructureWord)
        self.assertEqual(len(word.get_children()), 4)
