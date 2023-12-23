import os
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from logic_layer.text_structures.extracted_optical_text_structure.document_loading._exceptions import DocumentLoadingInputFileTypeException
from logic_layer.text_structures.extracted_optical_text_structure.document_loading._xml_loading import load_document_from_xml_format


class TestFunctionLoadDocumentFromXmlFormat(unittest.TestCase):

    def test_load_document_from_xml_format_with_valid_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('logic_layer.text_structures.extracted_optical_text_structure.document_loading._xml_loading.ET') as mock_et:
                mock_et.return_value.parse = lambda *args, **kwargs: ET.ElementTree()
                file_path = os.path.join(tmpdir, 'test.xml')
                with open(file_path, 'w') as output_file:
                    load_document_from_xml_format(output_file)

    def test_load_document_from_xml_format_with_invalid_file_type(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('logic_layer.text_structures.extracted_optical_text_structure.document_loading._xml_loading.ET') as mock_et:
                mock_et.return_value.parse = lambda *args, **kwargs: ET.ElementTree()
                file_path = os.path.join(tmpdir, 'test.json')
                with open(file_path, 'w') as output_file:
                    with self.assertRaises(DocumentLoadingInputFileTypeException):
                        load_document_from_xml_format(output_file)

