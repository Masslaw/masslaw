import unittest
import xml.etree.ElementTree as ET

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure.document_loading._xml_loading import _xml_element_to_structure_element


class TestFunctionXmlElementToStructureElement(unittest.TestCase):
    def test_xml_element_to_structure_element(self):
        line_element = ET.Element('ln')
        word1_element = ET.Element('wd')
        word1_element.set('v', 'hey')
        word2_element = ET.Element('wd')
        word2_element.set('v', 'there!')
        line_element.append(word1_element)
        line_element.append(word2_element)

        line = _xml_element_to_structure_element(line_element)

        self.assertIsInstance(line, OpticalTextStructureLine)
        self.assertEqual(len(line.get_children()), 2)
        self.assertEqual(line.get_children()[0].get_children(), list('hey'))
        self.assertEqual(line.get_children()[1].get_children(), list('there!'))
