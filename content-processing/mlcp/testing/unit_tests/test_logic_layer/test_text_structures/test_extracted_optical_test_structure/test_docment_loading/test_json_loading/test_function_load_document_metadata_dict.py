import unittest

from logic_layer.text_structures.extracted_optical_text_structure.document_loading._json_loading import _load_document_metadata_dict


class TestFunctionLoadDocumentMetadataDict(unittest.TestCase):

    def test_load_document_metadata_dict(self):
        metadata_dict = {
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
        }

        result_xml = _load_document_metadata_dict(metadata_dict)

        self.assertEqual(result_xml.tag, 'metadata')
        self.assertEqual(result_xml.attrib, {'type': 'optical'})
        self.assertEqual(len(result_xml), 2)
        self.assertEqual(result_xml[0].tag, 'subElement1')
        self.assertEqual(result_xml[1].tag, 'subElement2')
        self.assertEqual(result_xml[0].attrib, {'key': 'value1'})
        self.assertEqual(result_xml[1].attrib, {'key': 'value2'})
        self.assertEqual(len(result_xml[0]), 2)
        self.assertEqual(len(result_xml[1]), 0)
        self.assertEqual(result_xml[0][0].tag, 'metadataitem')
        self.assertEqual(result_xml[0][1].tag, 'metadataitem')
        self.assertEqual(result_xml[0][0].attrib, {'key': 'value1_1'})
        self.assertEqual(result_xml[0][1].attrib, {'key': 'value1_2'})
