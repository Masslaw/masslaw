import unittest
from xml.etree import ElementTree

from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._exceptions import DocumentExportingMetadataItemNoLabelException
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._xml_export import _metadata_item_to_xml_element


class TestFunctionMetadataItemToXmlElement(unittest.TestCase):

    def test_metadata_item_to_xml_element_valid_conditions(self):
        metadata_item = {"__label": "author", "name": "John Doe", "affiliation": "Fictional University", }

        xml_element = _metadata_item_to_xml_element(metadata_item)

        self.assertIsInstance(xml_element, ElementTree.Element)
        self.assertEqual(xml_element.tag, 'author')
        self.assertEqual(xml_element.get('name'), 'John Doe')
        self.assertEqual(xml_element.get('affiliation'), 'Fictional University')

    def test_metadata_item_to_xml_element_no_label(self):
        metadata_item = {"name": "John Doe", "affiliation": "Fictional University", }

        with self.assertRaises(DocumentExportingMetadataItemNoLabelException):
            _metadata_item_to_xml_element(metadata_item)
