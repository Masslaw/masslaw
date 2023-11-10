import os
import tempfile
import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._document import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting import DocumentExporter


class TestDocumentExporter(unittest.TestCase):

    def setUp(self):
        self.mock_document = ExtractedOpticalTextDocument(
            [OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER, ])
        self.document_exporter = DocumentExporter(document=self.mock_document)

    def test_export_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'test.json')
            with open(file_path, 'w') as output_file:
                self.document_exporter.export_json(opened_json_file=output_file)

    def test_export_xml(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'test.xml')
            with open(file_path, 'wb') as output_file:
                self.document_exporter.export_xml(opened_xml_file=output_file)

    def test_export_text(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, 'test.txt')
            with open(file_path, 'w') as output_file:
                self.document_exporter.export_text(opened_txt_file=output_file)
