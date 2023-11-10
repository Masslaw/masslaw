import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_cleanups._structure_cleanup_logic import cleanup_structure


class TestFunctionCleanupStructure(unittest.TestCase):
    def test_cleanup_structure(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Hello'))
        word1.set_bounding_rect((0, 0, 50, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('There'))
        word2.set_bounding_rect((45, 0, 95, 10))
        word3 = OpticalTextStructureWord()
        word3.set_children(list(''))
        word3.set_bounding_rect((100, 0, 150, 10))
        line1 = OpticalTextStructureLine()
        line1.set_children([word1, word2, word3])
        word4 = OpticalTextStructureWord()
        word4.set_children(list(''))
        word4.set_bounding_rect((0, 0, 50, 10))
        word5 = OpticalTextStructureWord()
        word5.set_children(list(''))
        word5.set_bounding_rect((45, 0, 95, 10))
        line2 = OpticalTextStructureLine()
        line2.set_children([word4, word5])
        group1 = OpticalTextStructureGroup()
        group1.set_children([line1, line2])

        structure = OpticalTextStructureRoot([OpticalTextStructureGroup, OpticalTextStructureLine, OpticalTextStructureWord])
        structure.set_children([group1])

        cleanup_structure(structure)

        self.assertEqual(len(structure.get_children()), 1)
        self.assertEqual(len(structure.get_children()[0].get_children()), 1)
        self.assertEqual(len(structure.get_children()[0].get_children()[0].get_children()), 2)
