import unittest
import xml.etree.ElementTree as ET

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure.document_loading._xml_loading import _xml_element_to_structure_root


class TestFunctionXmlElementToStructureRoot(unittest.TestCase):

    def test_xml_element_to_structure_root(self):
        xml_element = ET.Element('textStructure')
        xml_element.append(ET.Element('ln'))
        xml_element.append(ET.Element('ln'))

        structure = _xml_element_to_structure_root(xml_element)

        self.assertEqual(len(structure.get_children()), 2)
        self.assertIsInstance(structure.get_children()[0], OpticalTextStructureLine)
