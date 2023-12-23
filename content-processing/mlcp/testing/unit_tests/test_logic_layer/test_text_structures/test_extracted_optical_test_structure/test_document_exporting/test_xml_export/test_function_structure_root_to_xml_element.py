import unittest
from xml.etree import ElementTree

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._xml_export import _structure_root_to_xml_element


class TestFunctionStructureRootToXmlElement(unittest.TestCase):

    def create_dummy_structure_root(self):
        structure_root = OpticalTextStructureRoot()
        child_element = OpticalTextStructureElement()
        child_element.set_children(list("Dummy text"))
        structure_root.set_children([child_element])
        return structure_root

    def test_structure_root_to_xml_element_valid_conditions(self):
        structure_root = self.create_dummy_structure_root()
        result_element = _structure_root_to_xml_element(structure_root)

        self.assertIsInstance(result_element, ElementTree.Element)
        self.assertEqual('textStructure', result_element.tag)
        self.assertEqual('optical', result_element.attrib['type'])

    def test_structure_root_to_xml_element_with_children(self):
        structure_root = self.create_dummy_structure_root()
        result_element = _structure_root_to_xml_element(structure_root)

        children_elements = list(result_element)
        self.assertEqual(1, len(children_elements))
