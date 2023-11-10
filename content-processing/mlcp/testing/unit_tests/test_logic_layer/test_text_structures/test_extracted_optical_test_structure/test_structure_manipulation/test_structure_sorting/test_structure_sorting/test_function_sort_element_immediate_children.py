import unittest
from unittest.mock import patch

from logic_layer.bidi import ReadDirection
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_sorting._structure_sorting import sort_element_immediate_children


class TestFunctionSortElementImmediateChildren(unittest.TestCase):

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

        sort_element_immediate_children(structure)

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

        sort_element_immediate_children(structure)

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

        sort_element_immediate_children(structure)

        self.assertEqual([child.get_value() for child in structure.get_children()], [child1.get_value(), child2.get_value(), child3.get_value()])

    def test_correct_calls(self):
        group = OpticalTextStructureGroup()
        line = OpticalTextStructureLine()
        word = OpticalTextStructureWord()
        word.set_children(list('Hello'))
        word.set_bounding_rect((0, 0, 20, 10))
        line.set_children([word])
        group.set_children([line])

        with patch(
                'logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_sorting._structure_sorting.sort_elements_horizontally') as sort_elements_horizontally_mock:
            with patch(
                    'logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_sorting._structure_sorting.sort_elements_vertically') as sort_elements_vertically_mock:
                sort_element_immediate_children(group)
                sort_elements_vertically_mock.assert_called_once_with(elements=[line])
                sort_elements_horizontally_mock.assert_not_called()
                sort_elements_vertically_mock.reset_mock()
                sort_elements_horizontally_mock.reset_mock()
                sort_element_immediate_children(line)
                sort_elements_vertically_mock.assert_not_called()
                sort_elements_horizontally_mock.assert_called_once_with(elements=[word], direction=ReadDirection.LTR)
