import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._construction._construction_logic import construct_element_with_hierarchy


class TestFunctionConstructElementWithHierarchy(unittest.TestCase):

    def test_construction(self):
        word1 = OpticalTextStructureWord()
        word1.set_children(list('word1'))
        word1.set_bounding_rect((0, 0, 50, 10))
        word2 = OpticalTextStructureWord()
        word2.set_children(list('word2'))
        word2.set_bounding_rect((50, 0, 100, 10))
        word3 = OpticalTextStructureWord()
        word3.set_children(list('word3'))
        word3.set_bounding_rect((100, 0, 150, 10))
        word4 = OpticalTextStructureWord()
        word4.set_children(list('word4'))
        word4.set_bounding_rect((150, 0, 200, 10))
        word5 = OpticalTextStructureWord()
        word5.set_children(list('word5'))
        word5.set_bounding_rect((200, 0, 250, 10))
        word6 = OpticalTextStructureWord()
        word6.set_children(list('word6'))
        word6.set_bounding_rect((250, 0, 300, 10))
        word7 = OpticalTextStructureWord()
        word7.set_children(list('word7'))
        word7.set_bounding_rect((300, 0, 350, 10))
        word8 = OpticalTextStructureWord()
        word8.set_children(list('word8'))
        word8.set_bounding_rect((350, 0, 400, 10))
        word9 = OpticalTextStructureWord()
        word9.set_children(list('word9'))
        word9.set_bounding_rect((400, 0, 450, 10))
        word10 = OpticalTextStructureWord()
        word10.set_children(list('word10'))
        word10.set_bounding_rect((450, 0, 500, 10))
        line1 = OpticalTextStructureLine()
        line1.set_children([word1, word2])
        line1.set_bounding_rect((0, 0, 100, 10))
        line2 = OpticalTextStructureLine()
        line2.set_children([word3])
        line3 = OpticalTextStructureLine()
        line3.set_children([word4, word5, word6])
        line4 = OpticalTextStructureLine()
        line4.set_children([word7, word8])

        group1 = OpticalTextStructureGroup()
        group1.set_children([line1, line2])
        group1.set_bounding_rect((0, 0, 450, 10))

        hierarchy_formation = [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER]
        element = construct_element_with_hierarchy([group1, line3, line4, word9, word10], hierarchy_formation)

        self.assertEqual(len(element.get_children()), 6)
        self.assertEqual(len(element.get_children()[0].get_children()), 2)
        self.assertEqual(len(element.get_children()[1].get_children()), 1)
        self.assertEqual(len(element.get_children()[2].get_children()), 3)
        self.assertEqual(len(element.get_children()[3].get_children()), 2)
        self.assertEqual(len(element.get_children()[4].get_children()), 1)
        self.assertEqual(len(element.get_children()[5].get_children()), 1)
