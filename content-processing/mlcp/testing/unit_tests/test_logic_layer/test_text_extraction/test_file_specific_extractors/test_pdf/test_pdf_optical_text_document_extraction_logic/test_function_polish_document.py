import unittest
from unittest.mock import patch, MagicMock
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_extraction.file_specific_extractors.pdf._pdf_optical_text_document_extraction_logic import polish_document


class TestFunctionPolishDocument(unittest.TestCase):

    @patch('logic_layer.text_extraction.file_specific_extractors.pdf._pdf_optical_text_document_extraction_logic.OpticalTextStructureManipulator')
    def test_polish_document_calls(self, mock_manipulator_class):
        mock_document = MagicMock(spec=ExtractedOpticalTextDocument)
        mock_manipulator = mock_manipulator_class.return_value

        polish_document(mock_document)

        mock_manipulator_class.assert_called_once_with(mock_document)
        mock_manipulator.merge_mergeable_structure_children_sequentially.assert_called_once()
        mock_manipulator.clean_document_structure.assert_called_once()