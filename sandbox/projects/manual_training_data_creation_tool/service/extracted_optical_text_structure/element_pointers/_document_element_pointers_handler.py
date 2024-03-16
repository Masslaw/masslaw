from service.extracted_optical_text_structure import ExtractedOpticalTextDocument
from service.extracted_optical_text_structure import OpticalTextStructureElement
from service.extracted_optical_text_structure.element_pointers._element_pointers_logic import delete_element_at_pointer
from service.extracted_optical_text_structure.element_pointers._element_pointers_logic import get_element_at_pointer
from service.extracted_optical_text_structure.element_pointers._element_pointers_logic import set_element_at_pointer
from service.extracted_optical_text_structure._types import OpticalDocumentElementsPointer


class DocumentElementPointersHandler:

    def __init__(self, document: ExtractedOpticalTextDocument):
        self._document = document

    def get_element_at_pointer(self, pointer: OpticalDocumentElementsPointer):
        return get_element_at_pointer(structure=self._document.get_structure_root(), pointer=pointer)

    def delete_element_at_pointer(self, pointer: OpticalDocumentElementsPointer):
        return delete_element_at_pointer(structure=self._document.get_structure_root(), pointer=pointer)

    def set_element_at_pointer(self, pointer: OpticalDocumentElementsPointer, element: OpticalTextStructureElement):
        return set_element_at_pointer(structure=self._document.get_structure_root(), pointer=pointer, element=element)
