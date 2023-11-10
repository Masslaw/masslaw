import unittest
from xml.etree import ElementTree

from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._xml_export import _structure_element_to_xml_element


class TestFunctionStructureElementToXmlElement(unittest.TestCase):

    def test_structure_element_to_xml_element_valid_conditions(self):
        structure_element = OpticalTextStructureElement()
        structure_element.set_children(list("dummy text"))
        result_element = _structure_element_to_xml_element(structure_element)

        self.assertIsInstance(result_element, ElementTree.Element)
        self.assertEqual(structure_element.__class__.get_label(), result_element.tag)
        self.assertEqual(structure_element.get_value(), result_element.get('v'))

    def test_structure_element_to_xml_element_with_child_elements(self):
        structure_element = OpticalTextStructureElement()
        child_structure_element = OpticalTextStructureElement()
        child_structure_element.set_children(list("Child text"))
        structure_element.set_children([child_structure_element])

        result_element = _structure_element_to_xml_element(structure_element)
        children_elements = list(result_element)
        self.assertEqual(1, len(children_elements))
        self.assertEqual(child_structure_element.get_value(), children_elements[0].get('v'))
