import unittest

from logic_layer.text_structures.extracted_optical_text_structure import ExtractedOpticalTextDocument
from logic_layer.text_structures.extracted_optical_text_structure import OpticalStructureHierarchyLevel
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureGroup
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureLine
from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import OpticalTextStructureWord
from logic_layer.text_structures.extracted_optical_text_structure.element_pointers import DocumentElementPointersHandler
from logic_layer.text_structures.extracted_optical_text_structure.element_properties import DocumentElementsPropertiesManager


class TestClassDocumentElementsPropertiesManager(unittest.TestCase):

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

        self.properties_manager = DocumentElementsPropertiesManager(document=self.document)

        self.pointers_handler = DocumentElementPointersHandler(document=self.document)

    def test_set_properties_of_children(self):
        pointer = (0, 1, 0)
        self.properties_manager.set_element_property(pointer=pointer, property_name='dummy property', property_value='dummy value')
        self.properties_manager.set_element_property(pointer=pointer, property_name='another property', property_value='some value')

        target_element = self.pointers_handler.get_element_at_pointer(pointer=pointer)

        self.assertEqual(target_element.get_properties().get('dummy property'), 'dummy value')
        self.assertEqual(target_element.get_properties().get('another property'), 'some value')

    def test_get_properties_of_children(self):
        pointer = (0, 1, 0)
        target_element = self.pointers_handler.get_element_at_pointer(pointer=pointer)
        target_element.set_property(property_name='dummy property', property_value='dummy value')
        target_element.set_property(property_name='another property', property_value='some value')

        element_properties = self.properties_manager.get_element_properties(pointer=pointer)
        self.assertEqual(element_properties.get('dummy property'), 'dummy value')
        self.assertEqual(element_properties.get('another property'), 'some value')

    def test_delete_property_of_child(self):
        pointer = (0, 1, 0)
        target_element = self.pointers_handler.get_element_at_pointer(pointer=pointer)
        target_element.set_property(property_name='dummy property', property_value='dummy value')
        target_element.set_property(property_name='another property', property_value='some value')

        self.properties_manager.delete_element_property(pointer=pointer, property_name='dummy property')
        element_properties = target_element.get_properties()
        self.assertEqual(element_properties.get('dummy property'), None)
        self.assertEqual(element_properties.get('another property'), 'some value')
