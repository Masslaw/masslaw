import unittest

from logic_layer.bidi import ReadDirection
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_manipulation._structure_sorting._structure_sorting import sort_elements_horizontally


class TestFunctionSortElementsHorizontally(unittest.TestCase):
    def test_sort_elements_horizontally_ltf(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('Hello'))
        word1.set_bounding_rect((0, 0, 20, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('There'))
        word2.set_bounding_rect((20, 0, 40, 10))
        word3 = OpticalTextStructureWord()
        word3.set_children(list('Hru?'))
        word3.set_bounding_rect((40, 0, 60, 10))
        elements = [word2, word1, word3]

        sorted_elements = sort_elements_horizontally(elements, ReadDirection.LTR)
        self.assertEqual([e.get_value() for e in sorted_elements], [word1.get_value(), word2.get_value(), word3.get_value()])

    def test_sort_elements_horizontally_rtl(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('שלום'))
        word1.set_bounding_rect((40, 0, 60, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('לך'))
        word2.set_bounding_rect((20, 0, 40, 10))
        word3 = OpticalTextStructureWord()
        word3.set_children(list('חבר!'))
        word3.set_bounding_rect((0, 0, 20, 10))
        elements = [word2, word1, word3]

        sorted_elements = sort_elements_horizontally(elements, ReadDirection.RTL)
        self.assertEqual([e.get_value() for e in sorted_elements], [word1.get_value(), word2.get_value(), word3.get_value()])

    def test_sort_elements_horizontally_bidi(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('שלום'))
        word1.set_bounding_rect((40, 0, 60, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('לך'))
        word2.set_bounding_rect((20, 0, 40, 10))
        word3 = OpticalTextStructureWord()
        word3.set_children(list('Hello'))

        elements = [word2, word1, word3]
        sorted_elements = sort_elements_horizontally(elements, ReadDirection.RTL)
        self.assertEqual([e.get_value() for e in sorted_elements], [word1.get_value(), word2.get_value(), word3.get_value()])

        sorted_elements = sort_elements_horizontally(elements, ReadDirection.LTR)
        self.assertEqual([e.get_value() for e in sorted_elements], [word3.get_value(), word1.get_value(), word2.get_value()])
