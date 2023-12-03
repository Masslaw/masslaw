import unittest
from xml.etree import ElementTree

from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._exceptions import DocumentExportingNonDictionaryMetadataItemException
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._xml_export import _document_metadata_to_xml_element


class TestFunctionDocumentMetadataToXmlElement(unittest.TestCase):

    def test_document_metadata_to_xml_element_valid_conditions(self):
        metadata = {"details": {"__label": "details", "title": "Sample Document", "author": "Author Name", }, "publication": {"__label": "publication", "date": "2023-10-15", }, }

        xml_element = _document_metadata_to_xml_element(metadata)

        self.assertIsInstance(xml_element, ElementTree.Element)
        self.assertEqual(xml_element.tag, 'metadata')

        details_element = xml_element.find('details')
        self.assertIsNotNone(details_element)
        self.assertEqual(details_element.get('title'), 'Sample Document')
        self.assertEqual(details_element.get('author'), 'Author Name')

        publication_element = xml_element.find('publication')
        self.assertIsNotNone(publication_element)
        self.assertEqual(publication_element.get('date'), '2023-10-15')

    def test_document_metadata_to_xml_element_invalid_metadata_item(self):
        metadata = {"title": "Sample Document"}

        with self.assertRaises(DocumentExportingNonDictionaryMetadataItemException):
            _document_metadata_to_xml_element(metadata)
