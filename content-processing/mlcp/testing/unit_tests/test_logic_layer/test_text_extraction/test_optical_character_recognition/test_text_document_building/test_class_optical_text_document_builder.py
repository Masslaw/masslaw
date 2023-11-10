import unittest

from logic_layer.text_extraction.optical_character_recognition.text_document_building import OpticalTextDocumentBuilder
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel


class TestClassOpticalTextDocumentBuilder(unittest.TestCase):

    def test_document_construction(self):
        extracted_element_groups = [[("Hi", (0, 0, 10, 10)), ("There!", (10, 0, 20, 10)), ("How Are You?", (0, 10, 20, 20)), ],
            [("שלום", (0, 0, 10, 10)), ("לך", (10, 0, 20, 10)), ("איך אתה?", (0, 10, 10, 20)), ]]

        hierarchy_formation = [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, ]
        builder = OpticalTextDocumentBuilder(hierarchy_formation)
        document = builder.build_document_structure_from_ocr_extracted_elements(extracted_element_groups)
        structure = document.get_structure_root()

        self.assertIsInstance(document, ExtractedOpticalTextDocument)
        self.assertEqual(len(structure.get_children()), 2)
        self.assertEqual(len(structure.get_children()[0].get_children()), 3)
        self.assertEqual(len(structure.get_children()[0].get_children()[0].get_children()), 1)
        self.assertEqual(len(structure.get_children()[0].get_children()[1].get_children()), 1)
        self.assertEqual(len(structure.get_children()[0].get_children()[2].get_children()), 3)
        self.assertEqual(len(structure.get_children()[1].get_children()), 3)
        self.assertEqual(len(structure.get_children()[1].get_children()[0].get_children()), 1)
        self.assertEqual(len(structure.get_children()[1].get_children()[1].get_children()), 1)
        self.assertEqual(len(structure.get_children()[1].get_children()[2].get_children()), 2)
