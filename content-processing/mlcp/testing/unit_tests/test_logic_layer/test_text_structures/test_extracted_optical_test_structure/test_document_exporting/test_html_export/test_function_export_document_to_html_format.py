import unittest
import tempfile
from xml.etree import ElementTree

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._html_export import export_document_to_html_format
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._exceptions import DocumentExportingOutputFileTypeException


class TestFunctionExportDocumentToHtmlFormat(unittest.TestCase):

    def test_export_document_to_html_format_valid_conditions(self):
        optical_text_document = ExtractedOpticalTextDocument()
        with tempfile.NamedTemporaryFile('bw+', suffix='.html') as output_file:
            export_document_to_html_format(optical_text_document, output_file)
            output_file.seek(0)
            content = output_file.read()
            self.assertTrue('<div class="ml-document">' in content.decode())

    def test_export_document_to_html_format_invalid_file_type(self):
        optical_text_document = ExtractedOpticalTextDocument()
        with tempfile.NamedTemporaryFile('w+', suffix='.txt') as output_file:
            with self.assertRaises(DocumentExportingOutputFileTypeException):
                export_document_to_html_format(optical_text_document, output_file)
