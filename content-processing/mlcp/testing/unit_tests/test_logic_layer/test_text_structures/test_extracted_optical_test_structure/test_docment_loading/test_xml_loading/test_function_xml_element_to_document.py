import unittest
import xml.etree.ElementTree as ET

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure.document_loading._xml_loading import _xml_element_to_document


class TestFunctionXmlElementToDocument(unittest.TestCase):

    def test_function_xml_element_to_document(self):
        document_xml_element = ET.Element('document')
        document = _xml_element_to_document(document_xml_element)
        self.assertIsInstance(document, ExtractedOpticalTextDocument)