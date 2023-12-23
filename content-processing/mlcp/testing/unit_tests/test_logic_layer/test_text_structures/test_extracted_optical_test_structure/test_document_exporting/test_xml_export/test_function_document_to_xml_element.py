import unittest
from xml.etree import ElementTree

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._xml_export import _document_to_xml_element


class TestFunctionDocumentToXmlElement(unittest.TestCase):

    def test_document_to_xml_element_valid_conditions(self):
        optical_text_document = ExtractedOpticalTextDocument()
        result_element = _document_to_xml_element(optical_text_document)

        self.assertIsInstance(result_element, ElementTree.Element)
        self.assertEqual('extractedTextDocument', result_element.tag)
        self.assertEqual('optical', result_element.attrib['type'])

    def test_document_to_xml_element_check_structure(self):
        optical_text_document = ExtractedOpticalTextDocument()
        result_element = _document_to_xml_element(optical_text_document)

        structure_element = next((child for child in result_element if child.tag == 'textStructure'), None)
        self.assertIsNotNone(structure_element)
        self.assertEqual('optical', structure_element.attrib['type'])
