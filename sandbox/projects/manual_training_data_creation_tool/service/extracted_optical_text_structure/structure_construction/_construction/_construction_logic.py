from typing import List
from typing import Tuple
from typing import Type

from service.extracted_optical_text_structure._hierarchy_levels import hierarchy_level_to_element_class
from service.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from service.extracted_optical_text_structure._types import OpticalElementRawDataEntry
from service.extracted_optical_text_structure.structure_construction._structure_hierarchy_formation import OpticalStructureHierarchyFormation
from service.extracted_optical_text_structure.structure_construction._assertions import assert_elements_type
from service.extracted_optical_text_structure.structure_construction._assertions import assert_nested_children
from service.extracted_optical_text_structure.structure_construction._assertions import assert_non_empty_hierarchy_formation
from service.extracted_optical_text_structure.structure_construction._entry_handling import entry_handling


def get_appropriate_element_for_entry_in_structure_hierarchy(entry: OpticalElementRawDataEntry, hierarchy_formation: OpticalStructureHierarchyFormation) -> OpticalTextStructureElement:
    assert_non_empty_hierarchy_formation(hierarchy_formation=hierarchy_formation)
    element_type = hierarchy_formation[0]
    if len(hierarchy_formation) == 1:
        element_class = hierarchy_level_to_element_class(element_type)
        element_instance = element_class()
        element_instance.set_children(list(entry[0]))
        element_instance.set_bounding_rect(bounding_rect=entry[1])
        return element_instance
    child_entries = entry_handling.split_entry_by_element_type(entry=entry, element_type=element_type)
    if len(child_entries) == 1:
        return get_appropriate_element_for_entry_in_structure_hierarchy(entry=entry, hierarchy_formation=hierarchy_formation[1:])
    child_elements: List[OpticalTextStructureElement] = [get_appropriate_element_for_entry_in_structure_hierarchy(entry=child_entry, hierarchy_formation=hierarchy_formation[1:]) for child_entry in
                                                         child_entries]
    element_instance = construct_element_with_hierarchy(structure_elements=child_elements, hierarchy_formation=hierarchy_formation)
    return element_instance


def construct_element_with_hierarchy(structure_elements: List[OpticalTextStructureElement], hierarchy_formation: OpticalStructureHierarchyFormation):
    assert_non_empty_hierarchy_formation(hierarchy_formation=hierarchy_formation)
    assert_nested_children(structure_elements=structure_elements, hierarchy_formation=hierarchy_formation)
    element_type: Type = hierarchy_level_to_element_class(hierarchy_formation[0])
    child_type: Type = len(hierarchy_formation) > 1 and hierarchy_level_to_element_class(hierarchy_formation[1]) or str
    children: List[child_type] = []
    for structure_element in structure_elements:
        if structure_element.get_type() == element_type:
            children.extend(structure_element.get_children())
            continue
        if structure_element.get_type() == child_type:
            child = structure_element
            children.append(child)
            continue
        child = construct_element_with_hierarchy(structure_elements=[structure_element], hierarchy_formation=hierarchy_formation[1:])
        children.append(child)
    element = element_type()
    append_children_to_element(element, children)
    return element


def append_children_to_element(parent: OpticalTextStructureElement, children: List[OpticalTextStructureElement]):
    parent_children = parent.get_children()
    assert_elements_type(parent.get_children_type(), children)
    parent.set_children(parent_children + children)


def construct_element_from_structured_entries(structured_entries: List, hierarchy_formation: OpticalStructureHierarchyFormation) -> OpticalTextStructureElement:
    assert_non_empty_hierarchy_formation(hierarchy_formation=hierarchy_formation)
    element_type: Type = hierarchy_level_to_element_class(hierarchy_formation[0])
    children = []
    for child_part in structured_entries:
        if isinstance(child_part, List):
            child = construct_element_from_structured_entries(structured_entries=child_part, hierarchy_formation=hierarchy_formation[1:])
            children.append(child)
            continue
        if isinstance(child_part, Tuple):
            child = get_appropriate_element_for_entry_in_structure_hierarchy(entry=child_part, hierarchy_formation=hierarchy_formation[1:])
            children.append(child)
            continue
    element = element_type()
    element.set_children(children)
    return element
