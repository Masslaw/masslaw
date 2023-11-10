import unittest

from logic_layer.bidi import ReadDirection
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_sorting._structure_sorting import sort_ltr_sorted_elements_by_direction


class TestFunctionSortLRTSortedElementsByDirection(unittest.TestCase):

    def test_sort_ltr_sorted_elements_by_direction_with_ltr_text(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Hello'))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('There'))
        word3 = OpticalTextStructureWord()
        word3.set_children(list('Hru?'))

        ltr_sorted_elements = [word1, word2, word3]
        sorted_elements = sort_ltr_sorted_elements_by_direction(ltr_sorted_elements, ReadDirection.LTR)

        self.assertEqual([e.get_value() for e in sorted_elements], [word1.get_value(), word2.get_value(), word3.get_value()])

    def test_sort_ltr_sorted_elements_by_direction_with_rtl_text(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('שלום'))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('לך'))
        word3 = OpticalTextStructureWord()
        word3.set_children(list('חבר!'))

        ltr_sorted_elements = [word3, word2, word1]
        sorted_elements = sort_ltr_sorted_elements_by_direction(ltr_sorted_elements, ReadDirection.RTL)

        self.assertEqual([e.get_value() for e in sorted_elements], [word1.get_value(), word2.get_value(), word3.get_value()])

    def test_sort_ltr_sorted_elements_by_direction_with_bidi_text(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('שלום'))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('לך'))
        word3 = OpticalTextStructureWord()
        word3.set_children(list('John'))
        word4 = OpticalTextStructureWord()
        word4.set_children(list('Doe'))
        word5 = OpticalTextStructureWord()
        word5.set_children(list('מה'))
        word6 = OpticalTextStructureWord()
        word6.set_children(list('שלומך?'))

        ltr_sorted_elements = [word6, word5, word3, word4, word2, word1]
        sorted_elements = sort_ltr_sorted_elements_by_direction(ltr_sorted_elements, ReadDirection.RTL)

        self.assertEqual([e.get_value() for e in sorted_elements], [word1.get_value(), word2.get_value(), word3.get_value(), word4.get_value(), word5.get_value(), word6.get_value()])
