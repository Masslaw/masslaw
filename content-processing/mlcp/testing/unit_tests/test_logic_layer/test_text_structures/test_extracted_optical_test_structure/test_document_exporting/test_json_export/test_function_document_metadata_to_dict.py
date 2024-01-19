import unittest
import xml.etree.ElementTree as ET

from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._json_export import _document_metadata_to_dict


class TestFunctionDocumentMetadataToDict(unittest.TestCase):
    def test_function_document_metadata_to_dict(self):
        document_metadata = ET.Element('metadata')
        document_metadata.set('type', 'optical')
        sub_element_1 = ET.SubElement(document_metadata, 'subElement1')
        sub_element_1.set('key', 'value1')
        sub_element_2 = ET.SubElement(document_metadata, 'subElement2')
        sub_element_2.set('key', 'value2')
        sub_element_1_1 = ET.SubElement(sub_element_1, 'metadataitem')
        sub_element_1_1.set('key', 'value1_1')
        sub_element_1_2 = ET.SubElement(sub_element_1, 'metadataitem')
        sub_element_1_2.set('key', 'value1_2')

        metadata_dict = _document_metadata_to_dict(document_metadata)

        self.assertEqual(metadata_dict, {
            '__label': 'metadata',
            'type': 'optical',
            '__children': [
                {
                    '__label': 'subElement1',
                    'key': 'value1',
                    '__children': [
                        {
                            '__label': 'metadataitem',
                            'key': 'value1_1',
                            '__children': []
                        },
                        {
                            '__label': 'metadataitem',
                            'key': 'value1_2',
                            '__children': []
                        }
                    ]
                },
                {
                    '__label': 'subElement2',
                    'key': 'value2',
                    '__children': []
                }
            ]
        })