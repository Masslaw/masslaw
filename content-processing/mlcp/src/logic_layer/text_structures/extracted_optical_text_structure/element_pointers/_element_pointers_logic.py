from logic_layer.text_structures.extracted_optical_text_structure import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure.element_pointers._assertions import assert_non_empty_pointer
from logic_layer.text_structures.extracted_optical_text_structure.element_pointers._exceptions import InvalidPointerException
from logic_layer.text_structures.extracted_optical_text_structure._structure_root import OpticalTextStructureRoot
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalDocumentElementsPointer
from shared_layer.list_utils import list_utils


def get_element_at_pointer(structure: OpticalTextStructureRoot, pointer: OpticalDocumentElementsPointer) -> OpticalTextStructureElement:
    assert_non_empty_pointer(pointer=pointer)
    return _get_element_at_pointer_from_element(structure, pointer)


def delete_element_at_pointer(structure: OpticalTextStructureRoot, pointer: OpticalDocumentElementsPointer):
    assert_non_empty_pointer(pointer=pointer)
    target_element_parent = _get_element_at_pointer_from_element(structure, pointer[:-1])
    target_element_children = target_element_parent.get_children()
    target_element_children.pop(pointer[-1])


def set_element_at_pointer(structure: OpticalTextStructureRoot, pointer: OpticalDocumentElementsPointer, element: OpticalTextStructureElement):
    assert_non_empty_pointer(pointer=pointer)
    target_element_parent = _get_element_at_pointer_from_element(structure, pointer[:-1])
    target_element_allowed_type = target_element_parent.get_children_type()
    if target_element_allowed_type and not isinstance(element, target_element_allowed_type):
        raise ValueError(f"Element of type '{element.__class__.__name__}' is not allowed to be a child of an element with children of type '{target_element_allowed_type.__name__}'")
    target_element_children = target_element_parent.get_children()
    target_element_children[pointer[-1]] = element


def _get_element_at_pointer_from_element(element: OpticalTextStructureElement|OpticalTextStructureRoot, pointer: OpticalDocumentElementsPointer) -> OpticalTextStructureElement:
    if len(pointer) == 0: return element
    children = element.get_children()
    next_child = list_utils.get_element_at(children, pointer[0])
    if not next_child:
        raise InvalidPointerException(pointer=pointer, reason="Nested child not found")
    return _get_element_at_pointer_from_element(next_child, pointer[1:])
