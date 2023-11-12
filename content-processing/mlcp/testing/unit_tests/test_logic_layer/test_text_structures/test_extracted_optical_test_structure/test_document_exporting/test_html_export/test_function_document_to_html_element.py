import unittest
from xml.etree import ElementTree

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._html_export import _document_to_html_element


class TestFunctionDocumentToHtmlElement(unittest.TestCase):

    def test_document_to_html_element_valid_conditions(self):
        optical_text_document = ExtractedOpticalTextDocument(
            structure_hierarchy_formation=[OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER, ])
        result_element = _document_to_html_element(optical_text_document, [])

        self.assertIsInstance(result_element, ElementTree.Element)
        self.assertEqual('div', result_element.tag)
        self.assertEqual('ml-document', result_element.attrib['class'])

    def test_document_to_html_element_check_structure(self):
        optical_text_document = ExtractedOpticalTextDocument(
            structure_hierarchy_formation=[OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER, ])
        result_element = _document_to_html_element(optical_text_document, [])

        structure_element = next((child for child in result_element if child.tag == 'div' and child.attrib.get('class') == 'ml-document-structure'), None)
        self.assertIsNotNone(structure_element)
