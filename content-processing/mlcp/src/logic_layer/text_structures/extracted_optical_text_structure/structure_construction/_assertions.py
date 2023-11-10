from typing import List
from typing import Type

from logic_layer.text_structures.extracted_optical_text_structure._hierarchy_levels import hierarchy_level_to_element_class
from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureHierarchyFormation
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._exceptions import EmptyConstructionStructureHierarchyFormationException
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._exceptions import StructureConstructionElementNestingException
from logic_layer.text_structures.extracted_optical_text_structure.structure_construction._exceptions import StructureConstructionInvalidElementTypeException


def assert_nested_children(hierarchy_formation: OpticalStructureHierarchyFormation, structure_elements: List[OpticalTextStructureElement]):
    for child in structure_elements:
        assert_nested_child(hierarchy_formation=hierarchy_formation, child_instance=child)


def assert_nested_child(hierarchy_formation: OpticalStructureHierarchyFormation, child_instance: OpticalTextStructureElement):
    child_class = child_instance.__class__
    if child_class in [hierarchy_level_to_element_class(lvl) for lvl in hierarchy_formation]: return
    raise StructureConstructionElementNestingException(hierarchy_formation=hierarchy_formation, child_class=child_class)


def assert_elements_type(elements_type: Type, elements: List[OpticalTextStructureElement]):
    for element in elements:
        assert_element_type(element_type=elements_type, element_instance=element)


def assert_element_type(element_type: Type, element_instance: OpticalTextStructureElement):
    child_class = element_instance.__class__
    if child_class == (element_type or child_class): return
    raise StructureConstructionInvalidElementTypeException(expected_type=element_type, child_class=child_class.__class__)


def assert_non_empty_hierarchy_formation(hierarchy_formation: OpticalStructureHierarchyFormation):
    if len(hierarchy_formation) > 0: return
    raise EmptyConstructionStructureHierarchyFormationException()
