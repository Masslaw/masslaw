from typing import List
from typing import Type

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import hierarchy_level_to_element_class
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureHierarchyLevel


def collect_all_nested_children_of_type(
        element: OpticalTextStructureElement,
        elements_type: OpticalStructureHierarchyLevel
) -> List[OpticalTextStructureElement]:
    children = element.get_children()
    children_of_type = select_elements_of_type(children, elements_type)
    if element.is_leaf(): return children_of_type
    for child in children:
        children_of_type += collect_all_nested_children_of_type(child, elements_type)
    return children_of_type


def select_elements_of_type(
        elements: List[OpticalTextStructureElement],
        elements_type: OpticalStructureHierarchyLevel
) -> List[OpticalTextStructureElement]:
    element_class = hierarchy_level_to_element_class(elements_type)
    elements_of_type = [element for element in elements if isinstance(element, element_class)]
    return elements_of_type
