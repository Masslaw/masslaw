from typing import Dict

from service.extracted_optical_text_structure import ExtractedOpticalTextDocument
from service.extracted_optical_text_structure.element_pointers._document_element_pointers_handler import DocumentElementPointersHandler
from service.extracted_optical_text_structure._types import OpticalDocumentElementsPointer


class DocumentElementsPropertiesManager:

    def __init__(self, document: ExtractedOpticalTextDocument):
        self._document = document
        self._pointers_handler = DocumentElementPointersHandler(document=document)

    def get_element_properties(self, pointer: OpticalDocumentElementsPointer) -> Dict:
        element = self._pointers_handler.get_element_at_pointer(pointer=pointer)
        return element.get_properties()

    def set_element_property(self, pointer: OpticalDocumentElementsPointer, property_name: str, property_value: str):
        element = self._pointers_handler.get_element_at_pointer(pointer=pointer)
        element.set_property(property_name=property_name, property_value=property_value)
        self._pointers_handler.set_element_at_pointer(pointer=pointer, element=element)

    def delete_element_property(self, pointer: OpticalDocumentElementsPointer, property_name: str):
        element = self._pointers_handler.get_element_at_pointer(pointer=pointer)
        element.delete_property(property_name=property_name)
        self._pointers_handler.set_element_at_pointer(pointer=pointer, element=element)
