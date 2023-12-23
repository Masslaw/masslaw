import unittest
import xml.etree.ElementTree as ET

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure.document_loading._xml_loading import _determine_element_type_from_xml_element


class TestFunctionDetermineElementTypeFromXmlElement(unittest.TestCase):

    def test_determine_element_type_from_xml_element_with_valid_tag(self):
        xml_element = ET.Element('ln')
        child_type = _determine_element_type_from_xml_element(xml_element)
        self.assertEqual(child_type, OpticalTextStructureLine)

    def test_determine_element_type_from_xml_element_with_invalid_tag(self):
        xml_element = ET.Element('woooo')
        child_type = _determine_element_type_from_xml_element(xml_element)
        self.assertIsNone(child_type)
