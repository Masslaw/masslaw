import unittest

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.element_pointers._element_pointers_logic import get_element_at_pointer
from logic_layer.text_structures.extracted_optical_text_structure.element_pointers import document_element_pointers_exceptions


class TestFunctionGetElementAtPointer(unittest.TestCase):

    def setUp(self):
        self.document = ExtractedOpticalTextDocument()

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

    def test_get_element_at_pointer(self):
        pointer = (0, 1, 0)
        target_element = self.document.get_structure_root().get_children()[0].get_children()[1].get_children()[0]
        result_element = get_element_at_pointer(self.document.get_structure_root(), pointer=pointer)
        self.assertEqual(target_element, result_element)

    def test_with_invalid_pointer(self):
        pointer = (0, 3, 1)
        with self.assertRaises(document_element_pointers_exceptions.InvalidPointerException):
            get_element_at_pointer(self.document.get_structure_root(), pointer=pointer)

    def test_with_empty_pointer(self):
        pointer = ()
        with self.assertRaises(document_element_pointers_exceptions.InvalidPointerException):
            get_element_at_pointer(self.document.get_structure_root(), pointer=pointer)
