import unittest

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction import OpticalTextStructureConstructor


class TestClassOpticalTextStructureConstructor(unittest.TestCase):

    def test_add_entry_groups_to_structure(self):
        entry_groups = [[('Hello\nThere!', (65, 0, 115, 10)), ('How', (0, 20, 75, 30)), ('are you?', (90, 20, 130, 30))],
                        [('I am', (0, 0, 45, 10)), ('fine!', (0, 20, 50, 30)), ('Thank you.', (0, 40, 135, 50)), ]]

        document = ExtractedOpticalTextDocument(
            [OpticalStructureHierarchyLevel.PARAGRAPH, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER])

        structure_constructor = OpticalTextStructureConstructor(document)

        structure_constructor.add_entry_groups_to_structure(entry_groups)

        structure = document.get_structure_root()

        self.assertEqual(len(structure.get_children()), 2)
        self.assertEqual(len(structure.get_children()[0].get_children()), 4)
        self.assertEqual(len(structure.get_children()[0].get_children()[0].get_children()), 1)
        self.assertEqual(len(structure.get_children()[0].get_children()[0].get_children()[0].get_children()), 5)
        self.assertEqual(len(structure.get_children()[0].get_children()[1].get_children()), 1)
        self.assertEqual(len(structure.get_children()[0].get_children()[1].get_children()[0].get_children()), 6)
        self.assertEqual(len(structure.get_children()[0].get_children()[2].get_children()), 1)
        self.assertEqual(len(structure.get_children()[0].get_children()[2].get_children()[0].get_children()), 3)
        self.assertEqual(len(structure.get_children()[0].get_children()[3].get_children()), 2)
        self.assertEqual(len(structure.get_children()[0].get_children()[3].get_children()[0].get_children()), 3)
        self.assertEqual(len(structure.get_children()[0].get_children()[3].get_children()[1].get_children()), 4)

        self.assertEqual(len(structure.get_children()[1].get_children()[0].get_children()), 2)
        self.assertEqual(len(structure.get_children()[1].get_children()[0].get_children()[0].get_children()), 1)
        self.assertEqual(len(structure.get_children()[1].get_children()[0].get_children()[1].get_children()), 2)
        self.assertEqual(len(structure.get_children()[1].get_children()[1].get_children()), 1)
        self.assertEqual(len(structure.get_children()[1].get_children()[1].get_children()[0].get_children()), 5)
        self.assertEqual(len(structure.get_children()[1].get_children()[2].get_children()), 2)
        self.assertEqual(len(structure.get_children()[1].get_children()[2].get_children()[0].get_children()), 5)
        self.assertEqual(len(structure.get_children()[1].get_children()[2].get_children()[1].get_children()), 4)

    def test_add_structured_entry_groups_to_structure(self):
        structured_entry_groups = [
            [
                [
                    ('Hello', (0, 0, 50, 10)),
                    ('There!', (0, 20, 50, 30))
                ],
                [
                    ('How', (0, 0, 50, 10)),
                    ('are', (0, 20, 50, 30)),
                    ('you?', (0, 40, 50, 50))
                ]
            ],
            [
                [
                    ('I\'m', (0, 0, 50, 10)),
                    ('fine', (0, 20, 50, 30))
                ],
                [
                    ('Thank', (0, 0, 50, 10)),
                    ('you.', (0, 20, 50, 30))
                ]
            ]
        ]

        document = ExtractedOpticalTextDocument(
            [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER])

        structure_constructor = OpticalTextStructureConstructor(document)

        structure_constructor.add_structured_entry_groups_to_structure(structured_entry_groups)

        structure = document.get_structure_root()

        self.assertEqual(len(structure.get_children()), 2)
        self.assertEqual(len(structure.get_children()[0].get_children()), 2)
        self.assertEqual(len(structure.get_children()[0].get_children()[0].get_children()), 2)
        self.assertEqual(len(structure.get_children()[0].get_children()[0].get_children()[0].get_children()), 5)
        self.assertEqual(len(structure.get_children()[0].get_children()[0].get_children()[1].get_children()), 6)
        self.assertEqual(len(structure.get_children()[0].get_children()[1].get_children()), 3)
        self.assertEqual(len(structure.get_children()[0].get_children()[1].get_children()[0].get_children()), 3)
        self.assertEqual(len(structure.get_children()[0].get_children()[1].get_children()[1].get_children()), 3)
        self.assertEqual(len(structure.get_children()[0].get_children()[1].get_children()[2].get_children()), 4)
        self.assertEqual(len(structure.get_children()[1].get_children()), 2)
        self.assertEqual(len(structure.get_children()[1].get_children()[0].get_children()), 2)
        self.assertEqual(len(structure.get_children()[1].get_children()[0].get_children()[0].get_children()), 3)
        self.assertEqual(len(structure.get_children()[1].get_children()[0].get_children()[1].get_children()), 4)
        self.assertEqual(len(structure.get_children()[1].get_children()[1].get_children()), 2)
        self.assertEqual(len(structure.get_children()[1].get_children()[1].get_children()[0].get_children()), 5)
        self.assertEqual(len(structure.get_children()[1].get_children()[1].get_children()[1].get_children()), 4)
