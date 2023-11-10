import unittest

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_sorting._structure_sorting import sort_elements_top_to_bottom


class TestFunctionSortElementsTopToBottom(unittest.TestCase):

    def test_sort_elements_top_to_bottom_with_ltr_text(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Hello'))
        word1.set_bounding_rect((0, 0, 20, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('There'))
        word2.set_bounding_rect((0, 20, 40, 10))
        word3 = OpticalTextStructureWord()
        word3.set_children(list('Hru?'))
        word3.set_bounding_rect((0, 40, 60, 10))
        elements = [word2, word1, word3]

        sorted_elements = sort_elements_top_to_bottom(elements)
        self.assertEqual([e.get_value() for e in sorted_elements], [word1.get_value(), word2.get_value(), word3.get_value()])

    def test_sort_elements_top_to_bottom_with_rtl_text(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('שלום'))
        word1.set_bounding_rect((0, 40, 60, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('לך'))
        word2.set_bounding_rect((0, 20, 40, 10))
        word3 = OpticalTextStructureWord()
        word3.set_children(list('חבר!'))
        word3.set_bounding_rect((0, 0, 20, 10))
        elements = [word2, word1, word3]

        sorted_elements = sort_elements_top_to_bottom(elements)
        self.assertEqual([e.get_value() for e in sorted_elements], [word3.get_value(), word2.get_value(), word1.get_value()])

    def test_sort_elements_top_to_bottom_with_bidi_text(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('שלום'))
        word1.set_bounding_rect((0, 40, 60, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('לך'))
        word2.set_bounding_rect((0, 20, 40, 10))
        word3 = OpticalTextStructureWord()
        word3.set_children(list('Hello'))
        word3.set_bounding_rect((0, 0, 20, 10))
        elements = [word2, word1, word3]

        sorted_elements = sort_elements_top_to_bottom(elements)
        self.assertEqual([e.get_value() for e in sorted_elements], [word3.get_value(), word2.get_value(), word1.get_value()])
