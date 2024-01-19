import unittest
import xml.etree.ElementTree as ET

from logic_layer.text_structures.extracted_optical_text_structure.document_metadata._metadata_handling_logic import put_metadata_item


class TestFunctionPutMetadataItem(unittest.TestCase):

    def test_put_metadata_item(self):
        metadata_tree = ET.Element('metadata')
        metadata_tree = put_metadata_item(metadata_tree, ['a', 'b'], 'label1', {'d': 'e'})
        metadata_tree = put_metadata_item(metadata_tree, ['a', 'b', 'c'], 'label2', {'f': 'g'})
        metadata_tree = put_metadata_item(metadata_tree, ['x', 'y'], 'label3', {'h': 'i'})

        self.assertEqual(metadata_tree.tag, 'metadata')
        self.assertEqual(len(metadata_tree), 2)
        self.assertEqual(metadata_tree[0].tag, 'a')
        self.assertEqual(metadata_tree[1].tag, 'x')
        self.assertEqual(len(metadata_tree[0]), 1)
        self.assertEqual(len(metadata_tree[1]), 1)
        self.assertEqual(metadata_tree[0][0].tag, 'b')
        self.assertEqual(metadata_tree[1][0].tag, 'y')
        self.assertEqual(len(metadata_tree[0][0]), 2)
        self.assertEqual(len(metadata_tree[1][0]), 1)
        self.assertEqual(metadata_tree[0][0][0].tag, 'label1')
        self.assertEqual(metadata_tree[0][0][0].attrib, {'d': 'e'})
        self.assertEqual(metadata_tree[0][0][1].tag, 'c')
        self.assertEqual(len(metadata_tree[0][0][1]), 1)
        self.assertEqual(metadata_tree[0][0][1][0].tag, 'label2')
        self.assertEqual(metadata_tree[0][0][1][0].attrib, {'f': 'g'})
        self.assertEqual(metadata_tree[1][0][0].tag, 'label3')
        self.assertEqual(metadata_tree[1][0][0].attrib, {'h': 'i'})

    def test_with_empty_path(self):
        metadata_tree = ET.Element('metadata')
        metadata_tree = put_metadata_item(metadata_tree, [], 'label1', {'d': 'e'})

        self.assertEqual(metadata_tree.tag, 'label1')
        self.assertEqual(metadata_tree.attrib, {'d': 'e'})
