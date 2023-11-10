import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureParagraph
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_merging._sequential_merging import SequentialMerging


class TestClassSequentialMerging(unittest.TestCase):

    def test_sequential_merging_with_words(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Hel'))
        word1.set_bounding_rect((0, 0, 30, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('lo'))
        word2.set_bounding_rect((30, 0, 50, 10))
        word3 = OpticalTextStructureWord()
        word3.set_children(list('There!'))
        word3.set_bounding_rect((65, 0, 125, 10))
        line1 = OpticalTextStructureLine()
        line1.set_children([word1, word2, word3])

        merging_logic = SequentialMerging()
        merging_logic.merge_mergeable_element_children(line1)

        self.assertEqual(line1.get_value(), 'Hello There!')

    def test_sequential_merging_with_lines(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Hey'))
        word1.set_bounding_rect((0, 0, 30, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('whats'))
        word2.set_bounding_rect((65, 0, 125, 10))
        line1 = OpticalTextStructureLine()
        line1.set_children([word1, word2])
        word3 = OpticalTextStructureWord()
        word3.set_children(list('up?'))
        word3.set_bounding_rect((140, 0, 170, 10))
        line2 = OpticalTextStructureLine()
        line2.set_children([word3])
        group = OpticalTextStructureParagraph()
        group.set_children([line1, line2])

        merging_logic = SequentialMerging()
        merging_logic.merge_mergeable_element_children(group)

        self.assertEqual(group.get_value(), 'Hey whats up?')

    def test_sequential_merging_with_lines_and_words(self):
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
        group = OpticalTextStructureParagraph()
        group.set_children([line1, line2, line3])

        merging_logic = SequentialMerging()
        merging_logic.merge_mergeable_element_children(group)

        self.assertEqual(group.get_value(), 'Hey whats up?')

    def test_not_merging_words_with_character_size_diff(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Hey'))
        word1.set_bounding_rect((0, 0, 30, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('There'))
        word2.set_bounding_rect((30, 0, 130, 10))
        line1 = OpticalTextStructureLine()
        line1.set_children([word1, word2])

        merging_logic = SequentialMerging()
        merging_logic.merge_mergeable_element_children(line1)

        self.assertEqual(line1.get_value(), 'Hey There')

    def test_not_merging_words_with_height_diff(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Hey'))
        word1.set_bounding_rect((0, 0, 30, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('There'))
        word2.set_bounding_rect((30, 0, 80, 20))
        line1 = OpticalTextStructureLine()
        line1.set_children([word1, word2])

        merging_logic = SequentialMerging()
        merging_logic.merge_mergeable_element_children(line1)

        self.assertEqual(line1.get_value(), 'Hey There')

    def test_not_merging_lines_with_character_size_diff(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Hey'))
        word1.set_bounding_rect((0, 0, 30, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('There'))
        word2.set_bounding_rect((45, 0, 95, 10))
        line1 = OpticalTextStructureLine()
        line1.set_children([word1, word2])
        word3 = OpticalTextStructureWord()
        word3.set_children(list('whats'))
        word3.set_bounding_rect((95, 0, 195, 10))
        word4 = OpticalTextStructureWord()
        word4.set_children(list('up?'))
        word4.set_bounding_rect((255, 0, 315, 10))
        line2 = OpticalTextStructureLine()
        line2.set_children([word3, word4])
        group = OpticalTextStructureParagraph()
        group.set_children([line1, line2])

        merging_logic = SequentialMerging()
        merging_logic.merge_mergeable_element_children(group)

        self.assertEqual(group.get_value(), 'Hey There\nwhats up?')

    def test_not_merging_lines_with_height_diff(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Hey'))
        word1.set_bounding_rect((0, 0, 30, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('There'))
        word2.set_bounding_rect((45, 0, 95, 10))
        line1 = OpticalTextStructureLine()
        line1.set_children([word1, word2])
        word3 = OpticalTextStructureWord()
        word3.set_children(list('whats'))
        word3.set_bounding_rect((95, 0, 145, 20))
        word4 = OpticalTextStructureWord()
        word4.set_children(list('up?'))
        word4.set_bounding_rect((160, 0, 190, 20))
        line2 = OpticalTextStructureLine()
        line2.set_children([word3, word4])
        group = OpticalTextStructureParagraph()
        group.set_children([line1, line2])

        merging_logic = SequentialMerging()
        merging_logic.merge_mergeable_element_children(group)

        self.assertEqual(group.get_value(), 'Hey There\nwhats up?')
