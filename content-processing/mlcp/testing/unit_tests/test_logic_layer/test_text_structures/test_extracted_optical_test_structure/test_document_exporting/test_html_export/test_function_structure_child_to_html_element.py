import unittest
from unittest.mock import Mock, patch
from xml.etree import ElementTree

import numpy as np

from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure.document_exporting._html_export import _structure_child_to_html_element
from shared_layer.memory_utils.storage_cached_image import StorageCachedImage


class TestFunctionStructureChildToHtmlElement(unittest.TestCase):

    def test_structure_child_to_html_element_valid_conditions(self):
        structure_element = OpticalTextStructureElement(children=list("Sample Text"))
        html_element = _structure_child_to_html_element(structure_element)

        self.assertIsInstance(html_element, ElementTree.Element)
        self.assertEqual('div', html_element.tag)
        self.assertIn('position: relative;', html_element.attrib['style'])
        self.assertEqual('Sample Text', html_element.text)

    def test_structure_child_to_html_element_with_children(self):
        parent_element = OpticalTextStructureElement()
        child_element = OpticalTextStructureElement(children=list("Child"))
        parent_element.set_children([child_element])
        html_element = _structure_child_to_html_element(parent_element)

        self.assertEqual(len(html_element), 1)  # Check if there is one child element
        child_html_element = html_element[0]
        self.assertEqual(child_html_element.text, "Child")

    def test_structure_child_to_html_element_with_image(self):
        image = Mock(spec=StorageCachedImage)
        image_instance = Mock(spec=np.ndarray)
        image_instance.shape = [100, 200]
        image.get_image.return_value = image_instance

        with patch("logic_layer.text_structures.extracted_optical_text_structure.document_exporting._html_export.Image.fromarray") as from_array_patch:
            with patch("logic_layer.text_structures.extracted_optical_text_structure.document_exporting._html_export.base64.b64encode") as b64encode_patch:
                from_array_patch.return_value = Mock()
                b64encode_patch.return_value = Mock()
                b64encode_patch.return_value.decode.return_value = "DECODED_IMAGE"

                parent_element = OpticalTextStructureElement()
                html_element = _structure_child_to_html_element(parent_element, image)

                self.assertIn('position: relative;', html_element.attrib['style'])
                self.assertIn('height: 100px;', html_element.attrib['style'])
                self.assertIn('width: 200px;', html_element.attrib['style'])
                self.assertIn('background-image: url("data:image/png;base64,DECODED_IMAGE");', html_element.attrib['style'])