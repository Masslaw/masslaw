import unittest

from logic_layer.text_extraction.optical_character_recognition.text_document_building._construction_logic import construct_optical_text_document_from_structured_ocr_output
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel


class TestFunctionConstructOpticalTextDocumentFromStructuredOcrOutput(unittest.TestCase):
    def test_regular(self):
        structured_elements = [
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

        hierarchy_formation = [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER]

        constructed_document = construct_optical_text_document_from_structured_ocr_output(structure_hierarchy_formation=hierarchy_formation, extracted_structured_element_groups=structured_elements)

        structure = constructed_document.get_structure_root()

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
