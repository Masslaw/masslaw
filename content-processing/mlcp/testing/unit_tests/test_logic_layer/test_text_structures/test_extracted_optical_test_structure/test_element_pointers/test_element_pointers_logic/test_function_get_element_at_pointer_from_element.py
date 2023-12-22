import unittest

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.element_pointers._element_pointers_logic import _get_element_at_pointer_from_element
from logic_layer.text_structures.extracted_optical_text_structure.element_pointers.exceptions import InvalidPointerException


class TestFunctionGetElementAtPointerFromElement(unittest.TestCase):

    def setUp(self):
        self.document = ExtractedOpticalTextDocument([OpticalStructureHierarchyLevel.GROUP, OpticalStructureHierarchyLevel.LINE, OpticalStructureHierarchyLevel.WORD])

        element = OpticalTextStructureGroup(
            children=[
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(bounding_rect=(0, 0, 10, 10)),
                        OpticalTextStructureWord(bounding_rect=(20, 0, 30, 10))
                    ]
                ),
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(bounding_rect=(0, 20, 10, 30)),
                        OpticalTextStructureWord(bounding_rect=(30, 20, 40, 30))
                    ]
                ),
                OpticalTextStructureLine(
                    children=[
                        OpticalTextStructureWord(bounding_rect=(0, 50, 10, 60)),
                        OpticalTextStructureWord(bounding_rect=(40, 50, 50, 60))
                    ]
                ),
            ]
        )

        self.document.get_structure_root().set_children([element])

    def test__get_element_at_pointer_from_element(self):
        pointer = (1, 0)
        element = self.document.get_structure_root().get_children()[0]
        target_element = element.get_children()[1].get_children()[0]
        result_element = _get_element_at_pointer_from_element(element, pointer=pointer)
        self.assertEqual(target_element, result_element)

    def test_with_invalid_pointer(self):
        pointer = (0, 3, 1)
        element = self.document.get_structure_root().get_children()[0]
        with self.assertRaises(InvalidPointerException):
            _get_element_at_pointer_from_element(element, pointer=pointer)

    def test_with_pointer_too_long(self):
        pointer = (0, 1, 1, 0, 1)
        element = self.document.get_structure_root().get_children()[0]
        with self.assertRaises(InvalidPointerException):
            _get_element_at_pointer_from_element(element, pointer=pointer)

    def test_with_empty_pointer(self):
        pointer = ()
        _get_element_at_pointer_from_element(self.document.get_structure_root(), pointer=pointer)

    def test_get_element_at_pointer_from_structure_root(self):
        pointer = (0, 1, 0)
        target_element = self.document.get_structure_root().get_children()[0].get_children()[1].get_children()[0]
        result_element = _get_element_at_pointer_from_element(self.document.get_structure_root(), pointer=pointer)
        self.assertEqual(target_element, result_element)

    def test_with_empty_pointer_from_structure_root(self):
        pointer = ()
        element = _get_element_at_pointer_from_element(self.document.get_structure_root(), pointer=pointer)
        self.assertEqual(element, self.document.get_structure_root())