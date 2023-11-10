import unittest

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._txt_export import _get_plain_text_from_document


class TestFunctionGetPlainTextFromDocument(unittest.TestCase):

    def create_dummy_optical_text_document(self):
        optical_text_document = ExtractedOpticalTextDocument(
            structure_hierarchy_formation=[OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER, ])
        child_element = OpticalTextStructureElement()
        child_element.set_children(list("Dummy text"))
        optical_text_document.get_structure_root().set_children([child_element])
        return optical_text_document

    def test_get_plain_text_from_valid_document(self):
        optical_text_document = self.create_dummy_optical_text_document()
        result_text = _get_plain_text_from_document(optical_text_document)
        self.assertEqual(result_text.strip(), "Dummy text")

    def test_get_plain_text_from_empty_document(self):
        optical_text_document = ExtractedOpticalTextDocument(
            structure_hierarchy_formation=[OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER, ])
        result_text = _get_plain_text_from_document(optical_text_document)
        self.assertEqual(result_text.strip(), "")
