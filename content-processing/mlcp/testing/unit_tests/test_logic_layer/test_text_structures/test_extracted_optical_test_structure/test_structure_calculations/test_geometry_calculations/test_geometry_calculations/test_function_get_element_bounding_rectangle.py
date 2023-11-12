import unittest
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure.structure_calculations._geometry_calculations._structure_geometry_calculator import get_element_bounding_rectangle


class TestFunctionGetElementBoundingRectangle(unittest.TestCase):
    def test_bounding_rectangle_with_direct_rectangle(self):
        element = OpticalTextStructureElement()
        expected_rectangle = (10, 20, 30, 40)
        element.set_bounding_rect(expected_rectangle)

        result_rectangle = get_element_bounding_rectangle(element)
        self.assertEqual(result_rectangle, expected_rectangle)

    def test_bounding_rectangle_via_children(self):
        parent_element = OpticalTextStructureElement()
        child_element1 = OpticalTextStructureElement()
        child_element2 = OpticalTextStructureElement()

        child_element1.set_bounding_rect((5, 5, 15, 15))
        child_element2.set_bounding_rect((20, 20, 40, 40))
        parent_element.set_children([child_element1, child_element2])

        result_rectangle = get_element_bounding_rectangle(parent_element)
        self.assertEqual(result_rectangle, (5, 5, 40, 40))
