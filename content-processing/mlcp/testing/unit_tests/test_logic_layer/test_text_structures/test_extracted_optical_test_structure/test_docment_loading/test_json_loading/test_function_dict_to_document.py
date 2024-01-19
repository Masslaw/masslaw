import unittest

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure.document_loading._json_loading import _dict_to_document


class TestFunctionDictToDocument(unittest.TestCase):

    def test_function_dict_to_document(self):
        document_dict = {
            'textStructure': {},
            'metadata': {'__label': 'metadata', },
        }
        document = _dict_to_document(document_dict)
        self.assertIsInstance(document, ExtractedOpticalTextDocument)
