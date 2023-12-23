import unittest

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure.document_metadata import DocumentMetadataHandler


class TestClassDocumentMetadataHandler(unittest.TestCase):

    def test_put_metadata_items(self):
        document = ExtractedOpticalTextDocument()
        document_metadata_handler = DocumentMetadataHandler(document)

        document_metadata_handler.put_metadata_item(['a', 'b'], 'label1', {'d': 'e'})
        document_metadata_handler.put_metadata_item(['a', 'b', 'c'], 'label2', {'f': 'g'})
        document_metadata_handler.put_metadata_item(['x', 'y'], 'label3', {'h': 'i'})
        document_metadata_handler.put_metadata_item([], 'should_not_exist', {'k': 'l'})

        self.assertEqual(document.get_metadata(), {'a': {'b': {'__label': 'label1', 'c': {'__label': 'label2', 'f': 'g', }, 'd': 'e', }, }, 'x': {'y': {'__label': 'label3', 'h': 'i', }, }, })
