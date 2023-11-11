import unittest
from xml.etree import ElementTree

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument, OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._html_export import _structure_root_to_html_element


class TestFunctionStructureRootToHtmlElement(unittest.TestCase):

    def test_structure_root_to_html_element_valid_conditions(self):
        structure_root = OpticalTextStructureRoot(hierarchy_formation=[OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER])
        html_element = _structure_root_to_html_element(structure_root)

        self.assertIsInstance(html_element, ElementTree.Element)
        self.assertEqual('div', html_element.tag)
        self.assertEqual('ml-document-structure', html_element.attrib['class'])

    def test_structure_root_to_html_element_check_children(self):
        structure_root = OpticalTextStructureRoot(hierarchy_formation=[OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD, OpticalStructureHierarchyLevel.CHARACTER])
        html_element = _structure_root_to_html_element(structure_root)

        # Assuming children are present in the structure root, verify they are converted to HTML elements
        for child in structure_root.get_children():
            child_element = next((el for el in html_element if el.attrib.get('class') == child.__class__.get_label()), None)
            self.assertIsNotNone(child_element)
