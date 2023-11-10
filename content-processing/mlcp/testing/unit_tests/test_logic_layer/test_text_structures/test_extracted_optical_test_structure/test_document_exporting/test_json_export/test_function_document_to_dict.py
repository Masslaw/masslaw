import unittest

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._json_export import _document_to_dict


class TestDocumentToDictFunction(unittest.TestCase):

    def setUp(self):
        self.optical_text_document = ExtractedOpticalTextDocument(
            structure_hierarchy_formation=[OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER, ])

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
        self.optical_text_document.set_metadata({"author": "test_author", "value": "test_title"})
        result_dict = _document_to_dict(self.optical_text_document)
        self.assertEqual(result_dict['metadata'], {"author": "test_author", "value": "test_title"})
