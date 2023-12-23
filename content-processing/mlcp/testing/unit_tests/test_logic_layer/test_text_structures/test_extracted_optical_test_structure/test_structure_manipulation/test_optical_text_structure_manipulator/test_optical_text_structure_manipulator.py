import unittest

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation import OpticalTextStructureManipulator


class TestClassOpticalTextStructureManipulator(unittest.TestCase):
    def test_merge_mergeable_structure_children_sequentially(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Hey'))
        word1.set_bounding_rect((0, 0, 30, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('wha'))
        word2.set_bounding_rect((65, 0, 95, 10))
        line1 = OpticalTextStructureLine()
        line1.set_children([word1, word2])
        word3 = OpticalTextStructureWord()
        word3.set_children(list('ts'))
        word3.set_bounding_rect((95, 0, 115, 10))
        line2 = OpticalTextStructureLine()
        line2.set_children([word3])
        word4 = OpticalTextStructureWord()
        word4.set_children(list('up?'))
        word4.set_bounding_rect((130, 0, 160, 10))
        line3 = OpticalTextStructureLine()
        line3.set_children([word4])
        group1 = OpticalTextStructureGroup()
        group1.set_children([line1, line2, line3])

        word5 = OpticalTextStructureWord()
        word5.set_children(list('How'))
        word5.set_bounding_rect((0, 0, 30, 10))
        word6 = OpticalTextStructureWord()
        word6.set_children(list('are'))
        word6.set_bounding_rect((65, 0, 95, 10))
        line4 = OpticalTextStructureLine()
        line4.set_children([word5, word6])
        word4 = OpticalTextStructureWord()
        word4.set_children(list('you?'))
        word4.set_bounding_rect((110, 0, 150, 10))
        line5 = OpticalTextStructureLine()
        line5.set_children([word4])
        group2 = OpticalTextStructureGroup()
        group2.set_children([line4, line5])

        structure_root = OpticalTextStructureRoot()
        structure_root.set_children([group1, group2])

        document = ExtractedOpticalTextDocument()
        document.set_structure_root(structure_root)

        manipulator = OpticalTextStructureManipulator(document)
        manipulator.merge_mergeable_structure_children_sequentially()

        self.assertEqual(structure_root.get_children()[0].get_value(), 'Hey whats up?')
        self.assertEqual(structure_root.get_children()[1].get_value(), 'How are you?')

    def test_merge_mergeable_structure_children_using_rectangle_clustering(self):
        pass  # this capability is not yet implemented

    def test_clean_document_structure(self):
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

        structure = OpticalTextStructureRoot()
        structure.set_children([group1])

        document = ExtractedOpticalTextDocument()
        document.set_structure_root(structure)

        manipulator = OpticalTextStructureManipulator(document)
        manipulator.clean_document_structure()

        self.assertEqual(len(structure.get_children()), 1)
        self.assertEqual(len(structure.get_children()[0].get_children()), 1)
        self.assertEqual(len(structure.get_children()[0].get_children()[0].get_children()), 2)
