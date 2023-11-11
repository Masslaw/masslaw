import unittest
from xml.etree import ElementTree

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument, OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._html_export import _structure_element_to_html_element


class TestFunctionStructureElementToHtmlElement(unittest.TestCase):

    def test_structure_element_to_html_element_valid_conditions(self):
        structure_element = OpticalTextStructureElement(children=list("Sample Text"), bounding_rect=(0, 0, 100, 50))
        html_element = _structure_element_to_html_element(structure_element)

        self.assertIsInstance(html_element, ElementTree.Element)
        self.assertEqual('p', html_element.tag)
        self.assertIn('position: absolute;', html_element.attrib['style'])
        self.assertEqual('Sample Text', html_element.text)

    def test_structure_element_to_html_element_with_children(self):
        parent_element = OpticalTextStructureElement()
        child_element = OpticalTextStructureElement(children=list("Child"), bounding_rect=(0, 0, 100, 50))
        parent_element.set_children([child_element])
        html_element = _structure_element_to_html_element(parent_element)

        self.assertEqual(len(html_element), 1)  # Check if there is one child element
        child_html_element = html_element[0]
        self.assertEqual(child_html_element.text, "Child")
