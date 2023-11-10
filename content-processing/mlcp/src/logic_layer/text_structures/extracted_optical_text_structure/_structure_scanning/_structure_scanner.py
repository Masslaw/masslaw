from typing import List
from typing import Type

from logic_layer.text_structures.extracted_optical_text_structure._structure_element import OpticalTextStructureElement
from logic_layer.text_structures.extracted_optical_text_structure._structure_scanning._element_tree_traverse_logic import collect_all_nested_children_of_type
from logic_layer.text_structures.extracted_optical_text_structure._types import OpticalStructureHierarchyLevel


class OpticalTextStructureScanner:
    def __init__(self, element: OpticalTextStructureElement):
        self._element = element

    def collect_all_nested_children_of_type(self, elements_type: OpticalStructureHierarchyLevel) -> List[OpticalTextStructureElement]:
        return collect_all_nested_children_of_type(self._element, elements_type)

    def count_all_nested_children_of_type(self, elements_type: OpticalStructureHierarchyLevel) -> int:
        return len(collect_all_nested_children_of_type(self._element, elements_type))
