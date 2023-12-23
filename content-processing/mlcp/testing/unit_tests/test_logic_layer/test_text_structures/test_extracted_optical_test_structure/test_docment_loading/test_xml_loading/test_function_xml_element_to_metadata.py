import unittest
import xml.etree.ElementTree as ET

from logic_layer.text_structures.extracted_optical_text_structure.document_loading._xml_loading import _xml_element_to_metadata


class TestFunctionXmlElementToMetadata(unittest.TestCase):

    def test_function_xml_element_to_metadata(self):
        element = ET.Element('metadata')
        title_element = ET.Element('title')
        title_element.set('text',  'hey')
        element.append(title_element)
        page_sizes_element = ET.Element('pageSizes')
        page1_size_element = ET.Element('page1')
        page1_size_element.set('width', '100')
        page1_size_element.set('height', '200')
        page_sizes_element.append(page1_size_element)
        page2_size_element = ET.Element('page2')
        page2_size_element.set('width', '300')
        page2_size_element.set('height', '400')
        page_sizes_element.append(page2_size_element)
        element.append(page_sizes_element)

        metadata = _xml_element_to_metadata(element)

        self.assertEqual(metadata, {
            'title': {
                '__label': 'title',
                'text': 'hey'
            },
            'pageSizes': {
                '__label': 'pageSizes',
                'page1': {
                    '__label': 'page1',
                    'width': '100',
                    'height': '200'
                },
                'page2': {
                    '__label': 'page2',
                    'width': '300',
                    'height': '400'
                }
            }
        })
