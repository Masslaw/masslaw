import unittest
from unittest.mock import patch, MagicMock
from logic_layer.text_extraction.file_specific_extractors.pdf._pdf_optical_text_document_extraction_logic import extract_element_entries


class TestFunctionExtractElementEntries(unittest.TestCase):

    @patch('logic_layer.text_extraction.file_specific_extractors.pdf._pdf_optical_text_document_extraction_logic.pdfplumber.open')
    def test_extract_element_entries_valid_conditions(self, mock_pdf_open):
        mock_pdf = MagicMock()
        mock_pdf.__enter__.return_value = mock_pdf
        mock_pdf.pages = [MagicMock()]
        mock_pdf.pages[0].extract_text_lines.return_value = [{'text': 'Sample text', 'x0': 0, 'top': 0, 'x1': 100, 'bottom': 50}]
        mock_pdf.pages[0].width = 200
        mock_pdf.pages[0].height = 200
        mock_pdf_open.return_value = mock_pdf

        result = extract_element_entries('dummy_path.pdf')

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 1)
        self.assertEqual(result[0][0][0], 'Sample text')
