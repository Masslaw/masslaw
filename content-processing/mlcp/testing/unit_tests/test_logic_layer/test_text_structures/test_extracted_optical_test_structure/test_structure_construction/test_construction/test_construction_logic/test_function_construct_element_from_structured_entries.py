import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._exceptions import EmptyStructureHierarchyFormationException
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._construction._construction_logic import construct_element_from_structured_entries
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._exceptions import EmptyConstructionStructureHierarchyFormationException


class TestFunctionConstructElementFromStructuredEntries(unittest.TestCase):

    def test_valid(self):
        structured_entries = [
                [
                    ('Hello', (0, 0, 50, 10)),
                    ('There!', (0, 20, 50, 30))
                ],
                [
                    ('How', (0, 0, 50, 10)),
                    ('are', (0, 20, 50, 30)),
                    ('you?', (0, 40, 50, 50))
                ],
                [
                    ('I\'m', (0, 0, 50, 10)),
                    ('fine', (0, 20, 50, 30))
                ],
                [
                    ('Thank', (0, 0, 50, 10)),
                    ('you.', (0, 20, 50, 30))
                ]
            ]

        hierarchy_formation = [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER]

        constructed_element = construct_element_from_structured_entries(structured_entries=structured_entries, hierarchy_formation=hierarchy_formation)

        self.assertEqual(len(constructed_element.get_children()), 4)
        self.assertEqual(len(constructed_element.get_children()[0].get_children()), 2)
        self.assertEqual(len(constructed_element.get_children()[0].get_children()[0].get_children()), 5)
        self.assertEqual(len(constructed_element.get_children()[0].get_children()[1].get_children()), 6)
        self.assertEqual(len(constructed_element.get_children()[1].get_children()), 3)
        self.assertEqual(len(constructed_element.get_children()[1].get_children()[0].get_children()), 3)
        self.assertEqual(len(constructed_element.get_children()[1].get_children()[1].get_children()), 3)
        self.assertEqual(len(constructed_element.get_children()[1].get_children()[2].get_children()), 4)
        self.assertEqual(len(constructed_element.get_children()[2].get_children()), 2)
        self.assertEqual(len(constructed_element.get_children()[2].get_children()[0].get_children()), 3)
        self.assertEqual(len(constructed_element.get_children()[2].get_children()[1].get_children()), 4)
        self.assertEqual(len(constructed_element.get_children()[3].get_children()), 2)
        self.assertEqual(len(constructed_element.get_children()[3].get_children()[0].get_children()), 5)
        self.assertEqual(len(constructed_element.get_children()[3].get_children()[1].get_children()), 4)

    def test_structured_entry_hierarchy_not_matching_hierarchy_formation(self):
        structured_entries = [
                [
                    ('Hello', (0, 0, 50, 10)),
                    ('There!', (0, 20, 50, 30))
                ],
                [
                    ('How', (0, 0, 50, 10)),
                    ('are', (0, 20, 50, 30)),
                    ('you?', (0, 40, 50, 50))
                ],

                [
                    ('I\'m', (0, 0, 50, 10)),
                    ('fine', (0, 20, 50, 30))
                ],
                [
                    ('Thank', (0, 0, 50, 10)),
                    ('you.', (0, 20, 50, 30))
                ]
            ]

        hierarchy_formation = [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE]

        with self.assertRaises(EmptyConstructionStructureHierarchyFormationException):
            construct_element_from_structured_entries(structured_entries=structured_entries, hierarchy_formation=hierarchy_formation)
