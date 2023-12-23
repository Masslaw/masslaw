import os
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from logic_layer.text_structures.extracted_optical_text_structure.document_loading import DocumentLoader


class TestClassDocumentLoader(unittest.TestCase):
    def setUp(self):
        self.document_loader = DocumentLoader()

    def test_load_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('logic_layer.text_structures.extracted_optical_text_structure.document_loading._json_loading.json') as mock_json:
                mock_json.load = lambda *args, **kwargs: {}
                file_path = os.path.join(tmpdir, 'test.json')
                with open(file_path, 'w') as output_file:
                    self.document_loader.load_json(opened_json_file=output_file)

    def test_load_xml(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch('logic_layer.text_structures.extracted_optical_text_structure.document_loading._xml_loading.ET') as mock_element_tree:
                mock_element_tree.return_value.parse = lambda *args, **kwargs: ET.ElementTree()
                file_path = os.path.join(tmpdir, 'test.xml')
                with open(file_path, 'wb') as output_file:
                    self.document_loader.load_xml(opened_xml_file=output_file)