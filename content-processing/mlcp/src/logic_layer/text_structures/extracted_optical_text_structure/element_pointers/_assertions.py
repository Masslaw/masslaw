from logic_layer.text_structures.extracted_optical_text_structure.element_pointers.exceptions import InvalidPointerException
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalDocumentElementsPointer


def assert_non_empty_pointer(pointer: OpticalDocumentElementsPointer):
    if len(pointer) == 0:
        raise InvalidPointerException(pointer=pointer, reason="Pointer is empty")