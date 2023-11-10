import unittest

from logic_layer.text_structures.extracted_optical_text_structure._exceptions import StructureElementInvalidDefinitionException
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureElementOrderDirection


class TestClassOpticalTextStructureElement(unittest.TestCase):

    def test_get_label_returns_correct_label(self):
        element = OpticalTextStructureElement()
        self.assertEqual(element.get_label(), 'el')

    def test_children_management(self):
        element = OpticalTextStructureElement()
        self.assertTrue(element.is_empty())

        child1 = OpticalTextStructureElement()
        child2 = OpticalTextStructureElement()
        element.set_children([child1, child2])
        self.assertEqual(element.get_children(), [child1, child2])
        self.assertFalse(element.is_empty())

    def test_bounding_rectangle_management(self):
        element = OpticalTextStructureElement()
        self.assertEqual(element.get_bounding_rect(), (0, 0, 0, 0))  # No bounding rect set yet

        bounding_rect = (1, 2, 3, 4)
        element.set_bounding_rect(bounding_rect)
        self.assertEqual(element.get_bounding_rect(), bounding_rect)

    def test_value_representation(self):
        child1 = OpticalTextStructureElement()
        child1.set_children(['A'])
        child2 = OpticalTextStructureElement()
        child2.set_children(['B'])
        element = OpticalTextStructureElement(children=[child1, child2])
        self.assertEqual(element.get_value(), 'AB')  # Children's values are concatenated

    def test_leaf_detection(self):
        leaf_element = OpticalTextStructureElement()
        leaf_element.set_children(['Some text'])  # This is a leaf, so we can set a bounding rect
        self.assertTrue(leaf_element.is_leaf())

        non_leaf_element = OpticalTextStructureElement()
        child_element = OpticalTextStructureElement()
        non_leaf_element.set_children([child_element])
        self.assertFalse(non_leaf_element.is_leaf())

    def test_invalid_children_order_direction(self):
        class InvalidElement(OpticalTextStructureElement):
            _children_order_direction = 'invalid'  # Not a valid order direction

        with self.assertRaises(StructureElementInvalidDefinitionException):
            InvalidElement.assert_class_properties()

    def test_class_method_defaults(self):
        self.assertEqual(OpticalTextStructureElement.get_children_separator(), '')
        self.assertEqual(OpticalTextStructureElement.get_children_order_direction(), OpticalStructureElementOrderDirection.HORIZONTAL)
