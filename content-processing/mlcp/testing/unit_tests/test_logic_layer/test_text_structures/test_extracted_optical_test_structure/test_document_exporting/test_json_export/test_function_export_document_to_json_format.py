import json
import tempfile
import unittest

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._exceptions import DocumentExportingOutputFileTypeException
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._json_export import export_document_to_json_format


class TestExportDocumentToJsonFormat(unittest.TestCase):

    def setUp(self):
        self.optical_text_document = ExtractedOpticalTextDocument(
            structure_hierarchy_formation=[OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER, ])

    def test_export_to_json_valid_conditions(self):
        with tempfile.NamedTemporaryFile('w+', suffix='.json') as output_file:
            export_document_to_json_format(self.optical_text_document, output_file)
            output_file.seek(0)
            exported_content = json.load(output_file)
            self.assertIn('textStructure', exported_content)
            self.assertIn('metadata', exported_content)

    def test_export_to_json_invalid_file_type(self):
        with tempfile.NamedTemporaryFile('w+', suffix='.txt') as output_file:
            with self.assertRaises(DocumentExportingOutputFileTypeException):
                export_document_to_json_format(self.optical_text_document, output_file)

    def test_export_to_json_structure_content(self):
        with tempfile.NamedTemporaryFile('w+', suffix='.json') as output_file:
            export_document_to_json_format(self.optical_text_document, output_file)
            output_file.seek(0)
            exported_content = json.load(output_file)
            self.assertIsInstance(exported_content.get('textStructure'), dict)
            self.assertEqual(exported_content['textStructure']['type'], 'optical')
