import tempfile
import unittest

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._exceptions import DocumentExportingOutputFileTypeException
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._txt_export import export_document_to_txt_format


class TestFunctionExportDocumentToTxtFormat(unittest.TestCase):

    def create_dummy_optical_text_document(self):
        optical_text_document = ExtractedOpticalTextDocument(
            structure_hierarchy_formation=[OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER, ])
        child_element = OpticalTextStructureElement()
        child_element.set_children(list("Dummy text"))
        optical_text_document.get_structure_root().set_children([child_element])
        return optical_text_document

    def test_export_document_to_txt_format_valid_conditions(self):
        optical_text_document = self.create_dummy_optical_text_document()

        with tempfile.NamedTemporaryFile('w+', suffix='.txt') as output_file:
            export_document_to_txt_format(optical_text_document, output_file)
            output_file.seek(0)
            content = output_file.read()
            self.assertEqual(content.strip(), "Dummy text")

    def test_export_document_to_txt_format_invalid_file_type(self):
        optical_text_document = self.create_dummy_optical_text_document()

        with tempfile.NamedTemporaryFile('w+', suffix='.xml') as output_file:
            with self.assertRaises(DocumentExportingOutputFileTypeException):
                export_document_to_txt_format(optical_text_document, output_file)
