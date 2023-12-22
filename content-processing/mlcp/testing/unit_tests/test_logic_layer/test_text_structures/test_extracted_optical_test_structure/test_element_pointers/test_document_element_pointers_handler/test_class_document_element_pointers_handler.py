import unittest
from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.element_pointers import DocumentElementPointersHandler


class TestClassDocumentElementsPointersHandler(unittest.TestCase):

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

        self.pointers_handler = DocumentElementPointersHandler(document=self.document)

    def test_get_element_at_pointer(self):
        pointer = (0, 1, 0)
        target_element = self.pointers_handler.get_element_at_pointer(pointer=pointer)
        expected_element = self.document.get_structure_root().get_children()[0].get_children()[1].get_children()[0]
        self.assertEqual(target_element, expected_element)

    def test_delete_element_at_pointer(self):
        pointer = (0, 1, 0)
        self.pointers_handler.delete_element_at_pointer(pointer=pointer)
        self.assertEqual(len(self.document.get_structure_root().get_children()[0].get_children()[1].get_children()), 1)

    def test_set_element_at_pointer(self):
        pointer = (0, 1, 0)
        new_element = OpticalTextStructureWord(bounding_rect=(0, 0, 10, 10))
        self.pointers_handler.set_element_at_pointer(pointer=pointer, element=new_element)
        target_element = self.pointers_handler.get_element_at_pointer(pointer=pointer)
        self.assertEqual(target_element, new_element)


