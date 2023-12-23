import tempfile
import unittest

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._exceptions import DocumentExportingOutputFileTypeException
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._xml_export import export_document_to_xml_format


class TestFunctionExportDocumentToXmlFormat(unittest.TestCase):

    def test_export_document_to_xml_format_valid_conditions(self):
        optical_text_document = ExtractedOpticalTextDocument()
        with tempfile.NamedTemporaryFile('bw+', suffix='.xml') as output_file:
            export_document_to_xml_format(optical_text_document, output_file)
            output_file.seek(0)
            content = output_file.read()
            self.assertTrue(content.startswith(b'<?xml version=\'1.0\' encoding=\'utf-8\'?>'))
            self.assertIn(b'<extractedTextDocument type="optical">', content)

    def test_export_document_to_xml_format_invalid_file_type(self):
        optical_text_document = ExtractedOpticalTextDocument()
        with tempfile.NamedTemporaryFile('w+', suffix='.txt') as output_file:
            with self.assertRaises(DocumentExportingOutputFileTypeException):
                export_document_to_xml_format(optical_text_document, output_file)
