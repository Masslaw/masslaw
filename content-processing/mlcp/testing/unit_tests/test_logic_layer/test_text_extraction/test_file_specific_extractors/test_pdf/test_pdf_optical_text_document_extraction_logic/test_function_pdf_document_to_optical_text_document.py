import unittest
from unittest.mock import patch, Mock
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument, \
    OpticalStructureHierarchyFormation, OpticalStructureHierarchyLevel
from logic_layer.text_extraction.file_specific_extractors.pdf._pdf_optical_text_document_extraction_logic import pdf_document_to_optical_text_document


class TestFunctionPdfDocumentToOpticalTextDocument(unittest.TestCase):

    @patch('logic_layer.text_extraction.file_specific_extractors.pdf._pdf_optical_text_document_extraction_logic.extract_element_entries')
    @patch('logic_layer.text_extraction.file_specific_extractors.pdf._pdf_optical_text_document_extraction_logic.polish_document')
    def test_pdf_document_to_optical_text_document_valid_conditions(self, mock_polish_document, mock_extract_element_entries):
        mock_extract_element_entries.return_value = [[('Sample text', (0, 0, 1, 1))]]

        hierarchy_formation = [OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD]
        document = pdf_document_to_optical_text_document('dummy_path.pdf', hierarchy_formation)

        self.assertIsInstance(document, ExtractedOpticalTextDocument)
        self.assertEqual(document.get_structure_root().get_hierarchy_formation(), hierarchy_formation)
        self.assertEqual(len(document.get_structure_root().get_children()), 1)
        self.assertEqual(len(document.get_structure_root().get_children()[0].get_children()), 2)
        mock_extract_element_entries.assert_called_once_with('dummy_path.pdf')
        mock_polish_document.assert_called_once()
