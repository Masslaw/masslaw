import unittest
import xml.etree.ElementTree as ET

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._json_export import _document_to_dict


class TestDocumentToDictFunction(unittest.TestCase):

    def setUp(self):
        self.optical_text_document = ExtractedOpticalTextDocument()
        self.optical_text_document.get_structure_root().set_children([OpticalTextStructureLine()])

    def test_document_to_dict_valid_conditions(self):
        result_dict = _document_to_dict(self.optical_text_document)
        self.assertIsInstance(result_dict, dict)
        self.assertIn('textStructure', result_dict)
        self.assertIn('metadata', result_dict)

    def test_document_to_dict_structure_content(self):
        result_dict = _document_to_dict(self.optical_text_document)
        self.assertIsInstance(result_dict.get('textStructure'), dict)
        self.assertEqual(result_dict['textStructure']['type'], 'optical')

    def test_document_to_dict_with_metadata(self):
        metadata = self.optical_text_document.get_metadata()
        author = ET.SubElement(metadata, 'author')
        author.attrib = {'name': 'author'}
        title = ET.SubElement(metadata, 'title')
        title.attrib = {'value': 'title'}
        self.optical_text_document.set_metadata(metadata)
        result_dict = _document_to_dict(self.optical_text_document)
        self.assertEqual(result_dict['metadata'], {'__label': 'metadata', '__children': [{'__label': 'author', 'name': 'author', '__children': []}, {'__label': 'title', 'value': 'title', '__children': []}]})
