import unittest

from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure import optical_text_structure_exceptions
from logic_layer.text_structures.extracted_optical_text_structure._assertions import assert_child_type


class TestFunctionAssertChildType(unittest.TestCase):
    def test_assert_child_type_normal(self):
        assert_child_type(expected_type=OpticalStructureHierarchyLevel.GROUP, provided_type=OpticalStructureHierarchyLevel.GROUP)

    def test_assert_child_type_invalid(self):
        with self.assertRaises(optical_text_structure_exceptions.InvalidChildTypeException):
            assert_child_type(expected_type=OpticalStructureHierarchyLevel.GROUP, provided_type=OpticalStructureHierarchyLevel.LINE)

    def test_assert_child_type_none(self):
        with self.assertRaises(optical_text_structure_exceptions.InvalidChildTypeException):
            assert_child_type(expected_type=OpticalStructureHierarchyLevel.GROUP, provided_type=None)
