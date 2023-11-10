import unittest
from unittest.mock import patch

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_sorting._structure_sorting import sort_element_hierarchy


class TestFunctionSortElementHierarchy(unittest.TestCase):

    def test_sorting_element_hierarchy_ltr(self):
        structure = OpticalTextStructureLine()
        child1 = OpticalTextStructureWord()
        child1.set_children(list('Hello'))
        child1.set_bounding_rect((0, 0, 20, 10))
        child2 = OpticalTextStructureWord()
        child2.set_children(list('There'))
        child2.set_bounding_rect((20, 0, 40, 10))
        child3 = OpticalTextStructureWord()
        child3.set_children(list('Hru?'))
        child3.set_bounding_rect((20, 0, 40, 10))
        structure.set_children([child2, child3, child1])

        sort_element_hierarchy(structure)

        self.assertEqual([child.get_value() for child in structure.get_children()], [child1.get_value(), child2.get_value(), child3.get_value()])

    def test_sorting_element_hierarchy_rtl(self):
        structure = OpticalTextStructureLine()
        child1 = OpticalTextStructureWord()
        child1.set_children(list('שלום'))
        child1.set_bounding_rect((20, 0, 40, 10))
        child2 = OpticalTextStructureWord()
        child2.set_children(list('לך'))
        child2.set_bounding_rect((20, 0, 40, 10))
        child3 = OpticalTextStructureWord()
        child3.set_children(list('חבר!'))
        child3.set_bounding_rect((0, 0, 20, 10))
        structure.set_children([child2, child3, child1])

        sort_element_hierarchy(structure)

        self.assertEqual([child.get_value() for child in structure.get_children()], [child1.get_value(), child2.get_value(), child3.get_value()])

    def test_sorting_element_hierarchy_bidi(self):
        structure = OpticalTextStructureLine()
        child1 = OpticalTextStructureWord()
        child1.set_children(list('שלום'))
        child1.set_bounding_rect((20, 0, 40, 10))
        child2 = OpticalTextStructureWord()
        child2.set_children(list('לך'))
        child2.set_bounding_rect((20, 0, 40, 10))
        child3 = OpticalTextStructureWord()
        child3.set_children(list('Hello'))
        child3.set_bounding_rect((0, 0, 20, 10))
        structure.set_children([child2, child3, child1])

        sort_element_hierarchy(structure)

        self.assertEqual([child.get_value() for child in structure.get_children()], [child1.get_value(), child2.get_value(), child3.get_value()])

    def test_sorting_element_hierarchy_nested(self):
        group1 = OpticalTextStructureGroup()
        line1 = OpticalTextStructureLine()
        line2 = OpticalTextStructureLine()
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Line'))
        word1.set_bounding_rect((0, 0, 20, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('One'))
        word2.set_bounding_rect((20, 0, 40, 10))
        line1.set_children([word2, word1])
        word3 = OpticalTextStructureWord()
        word3.set_children(list('Line'))
        word3.set_bounding_rect((0, 10, 20, 20))
        word4 = OpticalTextStructureWord()
        word4.set_children(list('Two'))
        word4.set_bounding_rect((20, 10, 40, 20))
        line2.set_children([word4, word3])
        group1.set_children([line2, line1])

        sort_element_hierarchy(group1)

        self.assertEqual([word.get_value() for line in group1.get_children() for word in line.get_children()], [word1.get_value(), word2.get_value(), word3.get_value(), word4.get_value()])

    def test_correct_function_calls(self):
        group1 = OpticalTextStructureGroup()
        line1 = OpticalTextStructureLine()
        line2 = OpticalTextStructureLine()
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Line'))
        word1.set_bounding_rect((0, 0, 20, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('One'))
        word2.set_bounding_rect((20, 0, 40, 10))
        line1.set_children([word2, word1])
        word3 = OpticalTextStructureWord()
        word3.set_children(list('Line'))
        word3.set_bounding_rect((0, 10, 20, 20))
        word4 = OpticalTextStructureWord()
        word4.set_children(list('Two'))
        word4.set_bounding_rect((20, 10, 40, 20))
        line2.set_children([word4, word3])
        group1.set_children([line2, line1])

        with patch('logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_sorting._structure_sorting.sort_element_hierarchy') as mock_sort_element_hierarchy:
            mock_sort_element_hierarchy.side_effect = lambda *args, **kwargs: mock_sort_element_hierarchy.return_value

            sort_element_hierarchy(group1)

            mock_sort_element_hierarchy.assert_any_call(line1)
            mock_sort_element_hierarchy.assert_any_call(line2)

        with patch(
                'logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_sorting._structure_sorting.sort_element_immediate_children') as sort_element_immediate_children:
            sort_element_immediate_children.side_effect = lambda *args, **kwargs: sort_element_immediate_children.return_value

            sort_element_hierarchy(group1)

            sort_element_immediate_children.assert_any_call(group1)
            sort_element_immediate_children.assert_any_call(line1)
            sort_element_immediate_children.assert_any_call(line2)
