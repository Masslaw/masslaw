import unittest
from unittest.mock import MagicMock
from logic_layer.text_extraction.file_specific_extractors.pdf._pdf_optical_text_document_extraction_logic import get_text_elements_from_page


class TestFunctionGetTextElementsFromPage(unittest.TestCase):

    def test_get_text_elements_from_page_valid_conditions(self):
        mock_page = MagicMock()
        mock_page.extract_text_lines.return_value = [{'text': 'Sample text', 'x0': 0, 'top': 0, 'x1': 100, 'bottom': 50}]
        mock_page.width = 200
        mock_page.height = 200

        result = get_text_elements_from_page(mock_page)

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], 'Sample text')
        self.assertEqual(result[0][1], (0, 0, 0.5, 0.25))
